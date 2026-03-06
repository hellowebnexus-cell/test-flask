from flask import Flask, render_template, jsonify
import random
import string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate')
def generate_random():
    length = 16
    # Avoid visually similar characters for better readability
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    random_string = ''.join(random.choice(characters) for i in range(length))
    return jsonify({'result': random_string})

if __name__ == '__main__':
    app.run(debug=True,port=5000)
