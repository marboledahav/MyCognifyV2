from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import openai
import os

app = Flask(__name__)
CORS(app)
openai.api_key = os.environ.get('OPENAI_API_KEY')  # Replace with your OpenAI API key

def query_chat_model(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. You are helping students better understand content of complex texts by simplifying, explaining, defining, answering and giving insight."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    return response['choices'][0]['message']['content']

@app.route('/analyze', methods=['POST'])
@cross_origin()
def analyze_text():
    text = request.form.get('text')
    action = request.form.get('action')

    try:
        if action == 'Summarize':
            prompt = "Summarize the following text digestibly in as few words as you can, preferably no more than a sentence: " + text
            output = query_chat_model(prompt)
        elif action == 'Insight Analysis':
            prompt = "As a master of literature, make an analysis of the following text based on themes, symbols, etc... in as few words as possible: " + text
            output = query_chat_model(prompt)
        elif action == 'Simplest Explanation':
            prompt = "Explain the following text like you would to a 6 year old in as few words as possible: " + text
            output = query_chat_model(prompt)
        elif action == 'Detect Tone':
            prompt = "As a master linguist, describe the tone of the following text in as few words as possible: " + text
            output = query_chat_model(prompt)
        elif action == 'AnswerIt':
            prompt = "Answer the following question extremely concisely: " + text
            output = query_chat_model(prompt)
        elif action == 'Define Word':
            words = text.split()
            if len(words) != 1:
                return jsonify({"error": "Define Words option only works with single-word input"}), 400
            word = words[0]
            try:
                prompt = f"You are an expert lexicographer. Format your response the way you'd see it in the dictionary. Define the word: " + text
                output = query_chat_model(prompt)
            except Exception as e:
                output = {word: f"Error: {str(e)}"}
        else:
            return jsonify({"error": "Invalid action specified"}), 400

    except Exception as e:
        return jsonify({"error": "Could not analyze text: " + str(e)}), 500

    return jsonify({"output": output}), 200

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port, host='0.0.0.0')
