from fastapi import FastAPI
from api.routes import router
from logger import logger
from wasm_engine import wasm_engine

# TODO: Add API versioning support
# FIXME: Need to add proper CORS configuration for production
# Initialize FastAPI app
app = FastAPI()

# Include API routes
app.include_router(router)

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Starting OPA WASM API application")

    if wasm_engine.is_initialized():
        logger.info("OPA WASM engine is ready")
    else:
        # FIXME: Should raise exception or exit if WASM engine fails
        logger.warning("OPA WASM engine failed to initialize")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down OPA WASM API application")

if __name__ == "__main__":
    import uvicorn
uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

try:
    # Create proper function instantiations
    abort_func = wasmtime.Func(store, 
        wasmtime.FuncType([wasmtime.ValType.i32(), wasmtime.ValType.i32()], []),
        opa_abort)
        
    println_func = wasmtime.Func(store, 
        wasmtime.FuncType([wasmtime.ValType.i32(), wasmtime.ValType.i32()], [wasmtime.ValType.i32()]),
        opa_println)
        
    builtin3_func = wasmtime.Func(store, 
        wasmtime.FuncType([wasmtime.ValType.i32(), wasmtime.ValType.i32(), wasmtime.ValType.i32()], [wasmtime.ValType.i32()]),
        opa_builtin3)
    
    # Create imports in the format wasmtime 0.27.0 expects
    imports = [
        wasmtime.Extern.from_func(abort_func),
        wasmtime.Extern.from_func(println_func),
        wasmtime.Extern.from_func(builtin3_func)
    ]
    
    # For 0.27.0, we need to link imports not pass them directly
    linker = wasmtime.Linker(store)
    linker.define("env", "opa_abort", abort_func)
    linker.define("env", "opa_println", println_func) 
    linker.define("env", "opa_builtin3", builtin3_func)
    
    # Create instance using linker
    instance = linker.instantiate(module)
    
    logger.info("✅ OPA WASM initialized successfully")
    
except Exception as e:
    logger.error(f"❌ Failed to initialize OPA WASM: {e}")
    store = None
    instance = None

@app.get("/")
async def root():
    return {"message": "OPA WASM API"}

# --- Enhanced OPA Evaluation ---
def opa_eval(input_data):
    """Evaluate OPA policy using the OPA WASM evaluation API"""
    if not store or not instance:
        raise HTTPException(status_code=500, detail="OPA WASM module not initialized")
    
    try:
        exports = instance.exports(store)
        
        # Check what evaluation functions are available
        available_eval_funcs = [name for name in exports.keys() if 'eval' in name.lower()]
        logger.info(f"Available evaluation functions: {available_eval_funcs}")
        
        # Try different evaluation approaches
        if "opa_eval_ctx_new" in exports and "opa_eval" in exports:
            return evaluate_with_context_api(exports, input_data)
        elif "eval" in exports:
            return evaluate_with_simple_api(exports, input_data)
        else:
            logger.warning("No suitable evaluation function found, using fallback")
            return evaluate_simple_policy(input_data)
    
    except Exception as e:
        logger.error(f"Error during OPA evaluation: {e}")
        return evaluate_simple_policy(input_data)

def evaluate_with_context_api(exports, input_data):
    """Evaluate using the full OPA context API"""
    try:
        opa_malloc = exports["opa_malloc"]
        opa_free = exports["opa_free"]
        opa_eval_ctx_new = exports["opa_eval_ctx_new"]
        opa_eval_ctx_set_input = exports["opa_eval_ctx_set_input"]
        opa_eval_func = exports["opa_eval"]
        opa_eval_ctx_get_result = exports["opa_eval_ctx_get_result"]
        memory_export = exports["memory"]
        
        # Create evaluation context
        ctx = opa_eval_ctx_new(store)
        if not ctx:
            raise RuntimeError("Failed to create evaluation context")
        
        # Prepare input JSON
        input_json = json.dumps(input_data)
        input_bytes = input_json.encode('utf-8')
        
        # Allocate memory for input
        input_addr = opa_malloc(store, len(input_bytes))
        if not input_addr:
            raise RuntimeError("Failed to allocate memory")
        
        try:
            # Write input to memory
            memory_data = memory_export.data_ptr(store)
            memory_data[input_addr:input_addr + len(input_bytes)] = input_bytes
            
            # Set input and evaluate
            opa_eval_ctx_set_input(store, ctx, input_addr)
            opa_eval_func(store, ctx)
            
            # Get result
            result_addr = opa_eval_ctx_get_result(store, ctx)
            
            if result_addr:
                # Try to read and parse result
                result_data = memory_data[result_addr:result_addr + 1000]
                result_str = result_data.decode('utf-8', errors='ignore').rstrip('\x00')
                logger.info(f"Raw result: {result_str[:200]}")  # Debug output
                
                # Parse JSON result
                try:
                    result_json = json.loads(result_str)
                    # Look for the allow decision in the result
                    if isinstance(result_json, dict):
                        return bool(result_json.get('result', False))
                    return bool(result_json)
                except json.JSONDecodeError:
                    # Fallback: look for "true" in the result string
                    return "true" in result_str.lower()
            
            return False
        
        finally:
            opa_free(store, input_addr)
    
    except Exception as e:
        logger.error(f"Error in context API evaluation: {e}")
        raise

def evaluate_with_simple_api(exports, input_data):
    """Evaluate using simple eval function"""
    try:
        eval_func = exports["eval"]
        opa_malloc = exports.get("opa_malloc")
        opa_free = exports.get("opa_free")
        memory_export = exports["memory"]
        
        if not opa_malloc or not opa_free:
            logger.warning("malloc/free not available, using fallback")
            return evaluate_simple_policy(input_data)
        
        # Prepare input
        input_json = json.dumps(input_data)
        input_bytes = input_json.encode('utf-8')
        
        # Allocate and write input
        input_addr = opa_malloc(store, len(input_bytes))
        if not input_addr:
            return evaluate_simple_policy(input_data)
        
        try:
            memory_data = memory_export.data_ptr(store)
            memory_data[input_addr:input_addr + len(input_bytes)] = input_bytes
            
            # Call eval function
            result = eval_func(store, input_addr)
            logger.info(f"Simple eval result: {result}")
            
            return bool(result)
        
        finally:
            opa_free(store, input_addr)
    
    except Exception as e:
        logger.error(f"Error in simple API evaluation: {e}")
        return evaluate_simple_policy(input_data)

def evaluate_simple_policy(input_data):
    """Fallback policy evaluation implementing the Rego rule directly"""
    try:
        # Your Rego rule: default allow = false; allow if input.user.role == "admin"
        user_role = input_data.get("user", {}).get("role", "")
        allowed = user_role == "admin"
        logger.info(f"Fallback evaluation: user_role={user_role}, allowed={allowed}")
        return allowed
    except Exception as e:
        logger.error(f"Error in fallback evaluation: {e}")
        return False

# --- API Endpoints ---
@app.get("/resource")
async def get_resource(request: Request):
    """Protected resource endpoint"""
    user = {"role": "admin"}  # Change to "user" to test deny
    
    opa_input = {
        "user": user,
        "action": "read",
        "resource": "some_resource"
    }
    
    try:
        allowed = opa_eval(opa_input)
        if not allowed:
            raise HTTPException(status_code=403, detail="Access denied by policy")
        return {
            "message": "Access granted!",
            "user": user,
            "input": opa_input,
            "policy_result": allowed
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authorization failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    wasm_status = "initialized" if (store and instance) else "failed"
    return {
        "status": "healthy",
        "wasm_module": wasm_status,
        "timestamp": "2025-06-23"
    }

@app.get("/wasm-info")
async def wasm_info():
    """Get WASM module information"""
    if not store or not instance:
        return {"error": "WASM module not initialized"}
    
    try:
        exports = instance.exports(store)
        export_names = list(exports.keys())
        
        # Categorize exports
        opa_functions = [name for name in export_names if name.startswith('opa_')]
        eval_functions = [name for name in export_names if 'eval' in name.lower()]
        memory_functions = [name for name in export_names if 'malloc' in name or 'free' in name]
        
        return {
            "status": "initialized",
            "total_exports": len(export_names),
            "opa_functions": opa_functions[:20],  # Limit output
            "eval_functions": eval_functions,
            "memory_functions": memory_functions,
            "has_memory": "memory" in export_names
        }
    except Exception as e:
        return {"error": f"Failed to get WASM info: {e}"}

@app.get("/test-policy")
async def test_policy():
    """Test policy with different inputs"""
    test_cases = [
        {"user": {"role": "admin"}, "expected": True, "description": "Admin should be allowed"},
        {"user": {"role": "user"}, "expected": False, "description": "User should be denied"},
        {"user": {"role": "guest"}, "expected": False, "description": "Guest should be denied"},
        {"user": {}, "expected": False, "description": "No role should be denied"},
        {}, {"expected": False, "description": "No user should be denied"}
    ]
    
    results = []
    for i, test_case in enumerate(test_cases):
        opa_input = {
            "user": test_case.get("user", {}),
            "action": "read",
            "resource": f"test_resource_{i}"
        }
        
        try:
            allowed = opa_eval(opa_input)
            results.append({
                "test_id": i,
                "description": test_case["description"],
                "input": opa_input,
                "result": allowed,
                "expected": test_case["expected"],
                "passed": allowed == test_case["expected"]
            })
        except Exception as e:
            results.append({
                "test_id": i,
                "description": test_case["description"],
                "input": opa_input,
                "error": str(e),
                "expected": test_case["expected"],
                "passed": False
            })
    
    passed_count = sum(1 for r in results if r.get("passed", False))
    results_summary = {
        "total_tests": len(results),
        "passed": passed_count,
        "failed": len(results) - passed_count,
        "success_rate": f"{(passed_count/len(results)*100):.1f}%"
    }
    
    return {
        "summary": results_summary,
        "results": results
    }

@app.get("/debug-resource")
async def debug_resource():
    """Debug endpoint to test with different user roles"""
    test_roles = ["admin", "user", "guest", "moderator", None]
    results = {}
    
    for role in test_roles:
        user_data = {"role": role} if role else {}
        opa_input = {
            "user": user_data,
            "action": "read", 
            "resource": "debug_resource"
        }
        
        try:
            allowed = opa_eval(opa_input)
            results[f"role_{role or 'none'}"] = {
                "input": opa_input,
                "allowed": allowed,
                "status": "success"
            }
        except Exception as e:
            results[f"role_{role or 'none'}"] = {
                "input": opa_input,
                "allowed": False,
                "error": str(e),
                "status": "error"
            }
    
    # Calculate passed tests
    passed_count = sum(1 for result in results.values() if result.get("allowed", False))
    
    return {
        "debug_results": results,
        "wasm_initialized": store is not None and instance is not None,
        "summary": {
            "total_tests": len(results),
            "passed": passed_count,
            "failed": len(results) - passed_count,
            "success_rate": f"{(passed_count/len(results)*100):.1f}%"
        },
        "results": results
    }
