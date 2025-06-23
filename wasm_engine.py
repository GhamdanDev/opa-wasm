import wasmtime
from logger import logger
from config import POLICY_WASM_PATH

class WasmEngine:
    def __init__(self):
        self.store = None
        self.instance = None
        self.initialize()
    
    def initialize(self):
        """Initialize OPA WASM module with wasmtime"""
        try:
            # Create engine and store
            engine = wasmtime.Engine()
            self.store = wasmtime.Store(engine)
            module = wasmtime.Module.from_file(engine, POLICY_WASM_PATH)
            logger.info("✅ WASM module loaded successfully")
            
            # Define the host functions with correct signatures
            def opa_abort(caller, msg_ptr, msg_len):
                return None
                
            def opa_println(caller, msg_ptr, msg_len):
                return 0
            
            def opa_builtin3(caller, builtin_id, ctx, addr):
                return 0
            
            # Create proper function instantiations
            abort_func = wasmtime.Func(self.store, 
                wasmtime.FuncType([wasmtime.ValType.i32(), wasmtime.ValType.i32()], []),
                opa_abort)
                
            println_func = wasmtime.Func(self.store, 
                wasmtime.FuncType([wasmtime.ValType.i32(), wasmtime.ValType.i32()], [wasmtime.ValType.i32()]),
                opa_println)
                
            builtin3_func = wasmtime.Func(self.store, 
                wasmtime.FuncType([wasmtime.ValType.i32(), wasmtime.ValType.i32(), wasmtime.ValType.i32()], [wasmtime.ValType.i32()]),
                opa_builtin3)
            
            # Link imports
            linker = wasmtime.Linker(self.store)
            linker.define("env", "opa_abort", abort_func)
            linker.define("env", "opa_println", println_func) 
            linker.define("env", "opa_builtin3", builtin3_func)
            
            # Create instance using linker
            self.instance = linker.instantiate(module)
            
            logger.info("✅ OPA WASM initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize OPA WASM: {e}")
            self.store = None
            self.instance = None
    
    def get_exports(self):
        """Get WASM exports if initialized"""
        if not self.store or not self.instance:
            return None
        return self.instance.exports(self.store)
    
    def is_initialized(self):
        """Check if the WASM engine is initialized"""
        return self.store is not None and self.instance is not None

# Create a singleton instance
wasm_engine = WasmEngine()
