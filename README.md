# LLM + RAG-Based Function Execution API

## Overview
This project is a Flask-based API that retrieves and executes automation functions using LLM + RAG (Retrieval-Augmented Generation). It processes user text prompts & voice propmts, maps them to predefined functions, and generates executable Python code.

## Features
- Accepts user prompts and maps them to function calls.
- Uses LLM + RAG for intelligent function retrieval.
- Generates and executes Python scripts dynamically.
- Maintains session-based context for better responses.

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/YOUR_USERNAME/LLM-Function-Executor.git
   cd LLM-Function-Executor
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the Flask API:
   ```sh
   python app.py
   ```
4. Run Voice Client:
   ```sh
   cd client
   python voice_client.py 
   ```
4. Run text Client:
   ```sh
   cd client
   python text_client.py 
   ```

## Usage
Send a POST request to `/execute`:
```json
{
  "user_id": "123",
  "prompt": "Open calculator"
}
```

### Example Response:
```json
{
  "function": "open_calculator",
  "history": [{"prompt": "Open calculator", "function": "open_calculator"}]
}
```



## Author
**Baishnab Charan Behera**

## License
This project is licensed under the MIT License.
