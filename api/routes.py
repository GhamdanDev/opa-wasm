from fastapi import APIRouter, Request, HTTPException
from policy_evaluator import opa_eval
from wasm_engine import wasm_engine

# TODO: Add rate limiting to all endpoints
# FIXME: Need proper authentication middleware
router = APIRouter()

@router.get("/")
async def root():
    # TODO: Add API documentation link here
    return {"message": "OPA WASM API"}

@router.get("/resource")
async def get_resource(request: Request):
    """Protected resource endpoint"""
    # HACK: Hardcoded user role for testing
    # TODO: Extract user from JWT token or session
    user = {"role": "admin"}  # Change to "user" to test deny
    
    # FIXME: Need to validate input structure before passing to OPA
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

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    # TODO: Add more comprehensive health checks (memory, CPU, dependencies)
    wasm_status = "initialized" if wasm_engine.is_initialized() else "failed"
    # FIXME: Timestamp should be dynamic, not hardcoded
    return {
        "status": "healthy",
        "wasm_module": wasm_status,
        "timestamp": "2025-06-23"
    }

@router.get("/wasm-info")
async def wasm_info():
    """Get WASM module information"""
    if not wasm_engine.is_initialized():
        return {"error": "WASM module not initialized"}
    
    try:
        exports = wasm_engine.get_exports()
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

@router.get("/test-policy")
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

@router.get("/debug-resource")
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
        "wasm_initialized": wasm_engine.is_initialized(),
        "summary": {
            "total_tests": len(results),
            "passed": passed_count,
            "failed": len(results) - passed_count,
            "success_rate": f"{(passed_count/len(results)*100):.1f}%"
        },
        "results": results
    }
