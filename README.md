# Python Execution Service

## Requirements
- Docker
- Python 3.9+

# Python Executor Service

A secure Python script execution API deployed via Docker.

## Test Cases

### Working Examples (HTTP 200)

#### 1. Basic Arithmetic
```bash
curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{"script":"def main():\n    return {\"sum\": 2+2}"}'
```
Output: {"result": {"sum": 4}}

#### 2. String Manipulation
```bash
curl -X POST http://localhost:8080/execute \
    -H "Content-Type: application/json" \
    -d '{"script":"def main():\n    return {\"greeting\": \"Hello \".upper() + \"WORLD\".lower()}"}'
```
Output: {"result": {"greeting": "HELLO world"}}

#### 3. List Operations
```bash
curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{"script":"def main():\n    return {\"squares\": [x**2 for x in range(5)]}"}'
  ```
  Output: {"result": {"squares": [0, 1, 4, 9, 16]}}

#### 4. Dictionary Output
  ```bash
curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{"script":"def main():\n    return {\"user\": {\"name\": \"Alice\", \"age\": 25}}"}'
```
  Output: {"result": {"user": {"name": "Alice", "age": 25}}}

#### 5. Math Functions
```bash
curl -X POST http://localhost:8080/execute \
    -H "Content-Type: application/json" \
    -d '{"script":"import math\ndef main():\n    return {\"cosine\": math.cos(0)}"}'
  ```
  Output: {"result": {"cosine": 1.0}}


#### Error Cases (HTTP 400)

#### 6. Syntax Error
```bash
curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{"script":"def main():\n    return {"missing_quote: 1}"}'
  ```

  Output: {"error": "Script execution failed", "stderr": "SyntaxError: ..."}

#### 7. Missing main()
```bash
curl -X POST http://localhost:8080/execute \
    -H "Content-Type: application/json" \
    -d '{"script":"print(1+1)"}'
```
Output: {"error": "Script must contain a 'main()' function"}

#### 8. Dangerous Import (Blocked)
```bash
curl -X POST http://localhost:8080/execute \
    -H "Content-Type: application/json" \
    -d '{"script":"import os\ndef main():\n    return os.listdir()"}'
```
Output: {"error": "Dangerous imports detected"}

#### 9. Timeout
```bash
curl -X POST http://localhost:8080/execute \
    -H "Content-Type: application/json" \
    -d '{"script":"def main():\n    while True: pass"}'
```
Output: {"error": "Script execution timed out (15s limit)"}

#### 10. Empty Script
```bash
curl -X POST http://localhost:8080/execute \
    -H "Content-Type: application/json" \
    -d '{"script":""}'
```
Output: {"error": "Script cannot be empty"}


#### Edge Cases

#### 11. Boolean Logic
```bash
curl -X POST http://localhost:8080/execute \
    -H "Content-Type: application/json" \
    -d '{"script":"def main():\n    return {\"is_valid\": False or True}"}'
```
Output: {"result": {"is_valid": true}}

#### 12. None Handling
```bash
curl -X POST http://localhost:8080/execute \
    -H "Content-Type: application/json" \
    -d '{"script":"def main():\n    return {\"value\": None}"}'
```
Output: {"result": {"value": null}}

#### 13. Large Output
```bash
curl -X POST http://localhost:8080/execute \
    -H "Content-Type: application/json" \
    -d '{"script":"def main():\n    return {\"data\": [\"x\"]*1000}"}'
```
Output: {"result": {"data": ["x", "x", ... (1000 items)]}}

#### 14. Floating Point
```bash
curl -X POST http://localhost:8080/execute \
    -H "Content-Type: application/json" \
    -d '{"script":"def main():\n    return {\"pi\": 3.14159}"}'
```
  Output: {"result": {"pi": 3.14159}}

#### 15. Multi-line Script
```bash
curl -X POST http://localhost:8080/execute \
    -H "Content-Type: application/json" \
    -d '{"script":"def helper(x):\n    return x*2\ndef main():\n    return {\"doubled\": helper(21)}"}'  
``` 
Output: {"result": {"doubled": 42}}


## Quick Start
```bash
docker build -t python-executor .
docker run -p 8080:8080 python-executor