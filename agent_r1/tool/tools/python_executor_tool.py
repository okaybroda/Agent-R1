"""
Python executor tool implementation for executing Python code in a safe environment
"""

from typing import Dict
import json
import io
import sys
from agent_r1.tool.tool_base import Tool


class PythonExecutorTool(Tool):
    """
    Tool for executing Python code in a safe environment
    """
    
    def __init__(self):
        """
        Initialize the Python executor tool
        """
        name = "python_executor"
        description = "Execute Python code in a safe environment and return the output."
        parameters = {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Python code to execute. Must be a valid Python code block."
                }
            },
            "required": ["code"]
        }
        
        super().__init__(name, description, parameters)
    
    def execute(self, args: Dict) -> str:
        """
        Execute Python code in a safe environment
        
        Args:
            args: Tool parameters, containing:
                - "code": Python code to execute
            
        Returns:
            JSON string containing either the output or error message
        """
        code = args.get("code", "").strip()
        
        if not code:
            return json.dumps({"error": "No code provided."})
        
        try:
            # Create a safe environment with limited builtins
            safe_dict = {
                "abs": abs,
                "all": all,
                "any": any,
                "bin": bin,
                "bool": bool,
                "chr": chr,
                "dict": dict,
                "divmod": divmod,
                "enumerate": enumerate,
                "filter": filter,
                "float": float,
                "format": format,
                "frozenset": frozenset,
                "hash": hash,
                "hex": hex,
                "int": int,
                "isinstance": isinstance,
                "issubclass": issubclass,
                "iter": iter,
                "len": len,
                "list": list,
                "map": map,
                "max": max,
                "min": min,
                "next": next,
                "oct": oct,
                "ord": ord,
                "pow": pow,
                "print": print,
                "range": range,
                "repr": repr,
                "reversed": reversed,
                "round": round,
                "set": set,
                "slice": slice,
                "sorted": sorted,
                "str": str,
                "sum": sum,
                "tuple": tuple,
                "type": type,
                "zip": zip,
            }
            
            # Redirect stdout to capture output
            old_stdout = sys.stdout
            sys.stdout = output = io.StringIO()
            
            # Execute the code in the safe environment
            exec(code, {"__builtins__": safe_dict}, {})
            
            # Restore stdout and get the output
            sys.stdout = old_stdout
            output_str = output.getvalue()
            
            return json.dumps({"output": output_str})
            
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    def calculate_reward(self, args: Dict, result: str) -> float:
        """
        Calculate reward for Python code execution
        
        Args:
            args: Tool parameters
            result: Tool execution result
            
        Returns:
            Reward value
        """
        # Check if execution resulted in an error
        if "error" in result:
            return 0.05  # Small reward for trying
        
        if "No code provided" in result:
            return 0.0  # No reward for empty code
        
        # Base reward for successful execution
        reward = 0.4
        
        # Additional reward based on code complexity
        code = args.get("code", "")
        # Simple complexity metric: number of lines and operations
        complexity = len(code.split('\n')) + len([c for c in code if c in '+-*/()[]{}:'])
        
        # Additional reward based on complexity (with a cap)
        reward += min(0.1, 0.02 * complexity)
        
        return min(0.5, reward)  # Cap at 0.5


if __name__ == "__main__":
    python_executor = PythonExecutorTool()
    test_code = """
for i in range(5):
    print(f"Number: {i}")
"""
    print(python_executor.execute({"code": test_code}))
    print(python_executor.calculate_reward({"code": test_code}, '{"output": "Number: 0\\nNumber: 1\\nNumber: 2\\nNumber: 3\\nNumber: 4\\n"}')) 