from flask import Flask, render_template, request
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
    )

thread = client.beta.threads.create()

# Set up Flask app
app = Flask(__name__)

# Define the home page route
@app.route("/")
def home():
    return render_template("index.html")

# Define the Chatbot route
@app.route("/chatbot", methods=['POST'])
def chatbot():
    # Get the message input from the user
    user_input = request.form['message']
    
    # Use the OpenAI API to generate a response
    messages = [
        {"role": "system", "content": "You are a helpful assistant named Aguia."},
        {"role": "user", "content": user_input}
    ]
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content= user_input
    )

    # response = client.chat.completions.create(
    #     messages=messages,
    #     model="gpt-3.5-turbo",
    # )
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id="asst_x98YixiKKUXRSvbCsGTeLUw0",
        instructions="Você é um assistente da empresa grupo águia e deve auxiliar no treinamento de novos funcionários"
    )
    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        print(messages.data[0].content[0].text.value)


    # Extract the response text from the OpenAI API result
    #bot_response = response.choices[0].message.content
    bot_response = messages.data[0].content[0].text.value
    return render_template(
        "chatbot.html",
        user_input=user_input,
        bot_response=bot_response
    )

if __name__ == '__main__':
    app.run(debug=True)
