from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import openai 
import os

app = Flask(__name__)
CORS(app)
openai.api_key = os.environ.get('OPENAI_API_KEY')  # Replace with your OpenAI API key

@app.route('/analyze', methods=['POST'])
@cross_origin()
def analyze_text():
    text = request.form.get('text')
    action = request.form.get('action')

    try:
        if action == 'Summarize':
            prompt = "As a professor of English, please summarize the following text elegantly and understandably while also writing at a high level in less than 100 tokens: " + text
            response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=100, temperature=0.3)
            output = response.choices[0].text.strip()
        elif action == 'Insight Analysis':
            prompt = "As a master in philosophy and professor in literature, what are the key themes and insights in the following text elegantly and understandably while also writing at a high level in less than 100 tokens, take the style of the text itself and use context of the book in which the text is if it is in a book: " + text
            response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=100, temperature=0.3)
            output = response.choices[0].text.strip()
        elif action == 'Simplest Explanation':
            prompt = "You are a master linguist and have won awards in literature, please explain the following text in the simplest words possible in less than 100 tokens: " + text
            response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=100, temperature=0.2)
            output = response.choices[0].text.strip()
        elif action == 'Detect Tone':
            prompt = "As a master linguist, please analyze and describe the tone of the following text elegantly and understandably while also writing at a high level in less than 100 tokens: " + text
            response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=100, temperature=0.2)
            output = response.choices[0].text.strip()
        elif action == 'Define Word':
            words = text.split()
            if len(words) != 1:
                return jsonify({"error": "Define Words option only works with single-word input"}), 400
            word = words[0]
            try:
                prompt = f"You are an expert lexicographer. Format your response the way you'd see it in the dictionary. Define the word: " + text
                response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=100, temperature=0.0)
                output = response.choices[0].text.strip()
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
