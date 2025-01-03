from flask import Flask, jsonify, request
from litellm import completion
from litellm import completion_with_retries 
import os

## set ENV variables on your machine.

messages = [{ "content": "Hello, how are you?","role": "user"}]

# openai call
response = completion(model="gpt-4", messages=messages)

# cohere call
response = completion(model="command-r", messages=messages)
response = completion(model="command-nightly", messages=messages)

# Gemini call 
response = completion(model="gemini/gemini-pro", messages=messages)

# hugging face call
# e.g. Call 'WizardLM/WizardCoder-Python-34B-V1.0' hosted on HF Inference endpoints
# response = completion(
#   model="huggingface/WizardLM/WizardCoder-Python-34B-V1.0",
#   messages=[{ "content": "Hello, how are you?","role": "user"}], 
#   api_base="https://my-endpoint.huggingface.cloud"
# )

app = Flask(__name__)

# Example route
@app.route('/', methods=['GET'])
def hello():
    return jsonify(message="Hello, Flask!")

@app.route('/chat/completions', methods=["POST"])
def api_completion():
    data = request.json
    data["max_tokens"] = 1000 # By default let's set max_tokens to 256
    try:
        # COMPLETION CALL
        response = completion_with_retries(**data)
    except Exception as e:
        # print the error
        print(e)

    return response["choices"][0]["message"]["content"]

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=4000, threads=500)
