
from flask import Flask, jsonify, render_template, request
import openai
from decouple import config

# Set your OpenAI API key
API_KEY = config('API_KEY')
openai.api_key = API_KEY

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
    if(prompt[0]=='1'):
        print('short-response')
        prompt="Generate new short answers questions WHICH CAN BE INCLUDED IN A CUSTOM FEEDBACK FORM for a enterprises whose details are in the end IN THIS SPECIFIC FORMAT WITH THE DELIMITERs:QUESTION1\nQUESTION2\nQUESTION3\nQUESTION4\nQUESTION5\n The details of the enterprises are "+prompt
        chat_history = [
            {"role": "system", "content": "You are a chatbot"},
            {"role": "user", "content": prompt},
        ]
    
        # Generate a response from ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
        )
        response_messages = response['choices'][0]['message']['content']
        questions_list = response_messages.split('\n')
        print(questions_list)
        return jsonify({'questions': questions_list, 'options': []})
    if(prompt[0]=='2'):
        print('long-response')
        prompt="Generate new 'long' answers questions WHICH CAN BE INCLUDED IN A CUSTOM FEEDBACK FORM for a enterprises whose details are in the end IN THIS SPECIFIC FORMAT:QUESTION1\nQUESTION2\nQUESTION3\nQUESTION4\nQUESTION5\n DO NOT INCLUDE ANSWERS The details of the enterprises are "+prompt
        chat_history = [
            {"role": "system", "content": "You are a chatbot"},
            {"role": "user", "content": prompt},
        ]
    
        # Generate a response from ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
        )
        response_messages = response['choices'][0]['message']['content']
        print(response)
        questions_list = response_messages.split('\n\n')

        print(questions_list)
        return jsonify({'questions': questions_list, 'options': []})
    else:
        mquestions=[]
        moptions=[]
        existing_questions=""
        for i in range(1):
            # Create the chat conversation
            for x in mquestions:
                existing_questions+=x
            chat_history = [
                {"role": "system", "content": "You are a chatbot"},
                {"role": "user", "content": "Generate new which are not in"+ existing_questions+" MCQ QUESTIONS WHICH CAN BE INCLUDED IN A CUSTOM FEEDBACK FORM WITH OPTIONS ACCORDING TO THE STATEMENT IN THIS SPECIFIC FORMAT WITH THE DELIMITERS:QUESTION;OPTION1;OPTION2:OPTION3;OPTION4;\n " + prompt},
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
        print('why enter here')
        print(mquestions)
        print(moptions)
        return jsonify({'questions': mquestions, 'options': moptions})


if __name__ == '__main__':
    app.run(debug=True)
