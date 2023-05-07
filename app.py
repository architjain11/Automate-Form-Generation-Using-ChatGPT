
from flask import Flask, jsonify, render_template, request
import openai

# Set your OpenAI API key
openai.api_key = "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"

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        prompt = data['prompt']
    except KeyError:
        return jsonify({'error': 'Invalid request. Prompt not found.'}), 400
    mquestions = []
    moptions = []
    existing_questions = ""
    for i in range(1):
        # Create the chat conversation
        for x in mquestions:
            existing_questions += x
        chat_history = [
            {"role": "system", "content": "You are a chatbot"},
            {"role": "user", "content": "Generate new which are not in" + existing_questions +
                " MCQ QUESTIONS WHICH CAN BE INCLUDED IN A CUSTOM FEEDBACK FORM WITH OPTIONS ACCORDING TO THE STATEMENT IN THIS SPECIFIC FORMAT WITH THE DELIMITERS:QUESTION;OPTION1;OPTION2:OPTION3;OPTION4;\n " + prompt},
        ]

        # Generate a response from ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
        )

        result = response.choices[0].message.content
        result = result.strip()  # Remove leading/trailing whitespace

        # Split the result into questions and options
        questions = []
        options = []
        for item in result.split('\n'):
            if item:
                question, *opts = item.split(';')
                questions.append(question)
                options.append(opts[:-1])  # Remove the last empty option
        mquestions.extend(questions)
        moptions.extend(options)
    print(mquestions)
    print(moptions)
    return jsonify({'questions': mquestions, 'options': moptions})


if __name__ == '__main__':
    app.run(debug=True)
