from flask import Flask, render_template, jsonify
from flask.globals import request
import os

app = Flask(__name__)
data = {'text': ''}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/ping')
def ping():
    return 'pong!'


@app.route('/text')
def text():
    if os.path.exists('data.txt'):
        with  open("data.txt", "r") as f:
            data['text'] = f.read() 
    print('GET')
    print(data)
    return jsonify(data)


@app.route('/text', methods=['POST'])
def post_text():
    data = request.get_json()
    print('POST')
    print(data)
    with  open("data.txt", "w") as f:
        f.write(data['text'])
    return jsonify({'success': True})

# Run localy
# py -m flask run --host=0.0.0.0 --port=9797
# or run the mobpush.bat file

# Build image
# docker build --tag mobpush .

# Run container
# docker run -p 9797:5000 --name mobpush mobpush

# Run container in deattached mode
# docker run -d -p 9797:5000 --name mobpush mobpush

# Remove image (after stopping and removing all of its containers)
# docker rmi mobpush

if __name__ == '__main__':
    app.run(debug=True)
