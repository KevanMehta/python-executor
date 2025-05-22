import json
import subprocess
import tempfile
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

def validate_script(script):
    """Validate the script contains a main function."""
    if not script.strip():
        raise ValueError("Script cannot be empty")
    if "def main():" not in script:
        raise ValueError("Script must contain a 'main()' function")

def execute_script_safely(script):
    """Execute the script with proper Python syntax checking."""
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.py', delete=False) as f:
        # Write script with proper Python syntax and output handling
        f.write(f"""
import json
{script}

if __name__ == '__main__':
    result = main()
    if isinstance(result, dict):
        print(json.dumps(result))
    else:
        print(result)
""")
        temp_path = f.name
    
    try:
        result = subprocess.run(
            ['/usr/local/bin/python', temp_path],
            capture_output=True,
            text=True,
            timeout=15,
            env={'PYTHONPATH': ''}
        )
        return result
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)

@app.route('/execute', methods=['POST'])
def execute():
    try:
        data = request.get_json()
        if not data or 'script' not in data:
            return jsonify({'error': 'Invalid request, expected {"script": "..."}'}), 400
        
        script = data['script']
        validate_script(script)
        
        result = execute_script_safely(script)
        
        # Parse the output
        stdout = result.stdout.strip()
        if not stdout:
            return jsonify({
                'error': 'No output from main() function',
                'stdout': stdout,
                'stderr': result.stderr
            }), 400
            
        try:
            # First try direct JSON parsing
            output = json.loads(stdout)
            return jsonify({
                'result': output,
                'stdout': stdout,
                'stderr': result.stderr
            })
        except json.JSONDecodeError:
            # If direct parsing fails, try evaluating Python literals
            try:
                import ast
                output = ast.literal_eval(stdout)
                return jsonify({
                    'result': output,
                    'stdout': stdout,
                    'stderr': result.stderr
                })
            except (ValueError, SyntaxError):
                return jsonify({
                    'error': f'The output was not valid JSON or Python object: {stdout}',
                    'stdout': stdout,
                    'stderr': result.stderr
                }), 400
            
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Script execution timed out'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)