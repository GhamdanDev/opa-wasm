import json
from fastapi import HTTPException
from logger import logger
from wasm_engine import wasm_engine

# TODO: Add caching mechanism for policy evaluation results
# FIXME: Need to handle race conditions in concurrent evaluations
def opa_eval(input_data):
    """Evaluate OPA policy using the OPA WASM evaluation API"""
    if not wasm_engine.is_initialized():
        raise HTTPException(status_code=500, detail="OPA WASM module not initialized")
    
    try:
        exports = wasm_engine.get_exports()
        
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
        store = wasm_engine.store
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
        store = wasm_engine.store
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
    # HACK: Hardcoded policy logic, should be loaded from config
    # TODO: Make this configurable and support multiple policies
    try:
        # Your Rego rule: default allow = false; allow if input.user.role == "admin"
        user_role = input_data.get("user", {}).get("role", "")
        allowed = user_role == "admin"
        logger.info(f"Fallback evaluation: user_role={user_role}, allowed={allowed}")
        return allowed
    except Exception as e:
        logger.error(f"Error in fallback evaluation: {e}")
        # FIXME: Should not silently return False on error
        return False
