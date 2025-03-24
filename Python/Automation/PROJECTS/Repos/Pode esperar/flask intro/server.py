from flask import Flask, render_template, request
import numpy as np
from model import predict

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/roll-dice')
def roll_dice():
    rolls = [np.random.randint(1, 7) for _ in range(10)]
    return render_template('roll-dice.html', rolls=rolls)


@app.route('/my-first-form')
def my_first_form():
    return render_template('my-first-form.html')


@app.route('/for-response', methods=['POST'])
def handle_response():
    first_name = request.form['first_name']
    greeting = "Hi there, "

    # if first_name != '':
    #     greeting += first_name + ' '
    greeting += first_name + '!'

    return render_template('for-response.html', greeting=greeting)


@app.route('/write-message')
def write_message():
    return render_template('write-message.html')


@app.route('/deploy-model', methods=['POST'])
def deploy_model():
    message = request.form['message']
    prediction = "The message you wrote is: "
    prediction += message + '.'
    function = "Your message is "
    function += predict(message) + '!'

    return render_template('deploy-model.html', prediction=prediction, function=function)