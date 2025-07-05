from flask import Flask, request, jsonify
from core.query_to_function import get_function
import core.automation_function as af
import inspect

app = Flask(__name__)


@app.route("/execute", methods=["POST"])
def execute_function():
    data = request.json
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    # Get function name
    function_name = get_function(prompt)
    if not function_name:
        return jsonify({"error": "No matching function found"}), 404

    # Execute function
    try:
        fn = getattr(af, function_name)

        # Check if function needs parameters
        sig = inspect.signature(fn)
        if len(sig.parameters) > 0:
            # Extract parameters from prompt for functions that need them
            if function_name == "run_shell_command":
                # Extract command from prompt
                command = prompt.split("run", 1)[-1].strip()
                result = fn(command)
            elif function_name == "kill_process":
                # Extract process name
                process = prompt.split("kill", 1)[-1].strip()
                result = fn(process)
            elif function_name == "create_file":
                # Extract filename
                filename = prompt.split("create", 1)[-1].strip()
                result = fn(filename)
            else:
                return jsonify({"error": "Parameters required but not provided"}), 400
        else:
            result = fn()

        return jsonify({
            "function": function_name,
            "status": "success",
            "output": result
        })

    except Exception as e:
        return jsonify({
            "function": function_name,
            "status": "error",
            "output": str(e)
        }), 500


@app.route("/functions", methods=["GET"])
def list_functions():
    functions = [name for name in dir(af) if not name.startswith('_') and callable(getattr(af, name))]
    return jsonify({"available_functions": functions})


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
