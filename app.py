from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_question = data.get("question")
    
    if not user_question:
        return jsonify({"error": "No question provided"}), 400
    
    response = requests.post(
        'https://llm-beige.vercel.app/medical/invoke', 
        json={"input": {"question": user_question}}
    )
    
    if response.status_code == 200:
        bot_response = response.json().get("output", {}).get("text", "Error in response")
        return jsonify({"response": bot_response})
    else:
        return jsonify({"error": "Failed to fetch response from API"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)