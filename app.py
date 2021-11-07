from flask import Flask, json, render_template, jsonify, flash, redirect, send_from_directory
from flask.globals import request
import os
# from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './templates/docs'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx', 'pdf', 'xml', 'json', 'mp3', 'mp4', 'js', 'zip', 'rar'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = '8e532e20-84ea-400d-a4fb-96294e9416aa'
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
        with open("data.txt", "r") as f:
            data['text'] = f.read()
    print('GET')
    print(data)
    return jsonify(data)


@app.route('/text', methods=['POST'])
def post_text():
    data = request.get_json()
    print('POST')
    print(data)
    with open("data.txt", "w") as f:
        f.write(data['text'])
    return jsonify({'success': True})


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/docs/<name>', methods=["GET"])
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/docs/<name>/delete', methods=['POST'])
def delete_file(name):
    dir_name = app.config["UPLOAD_FOLDER"]
    filepath = os.path.join(dir_name, name)
    if not os.path.isfile(filepath) or '/' in name:
        return jsonify({"success": False})
    os.remove(filepath)
    return jsonify({"success": True})

@app.route('/docs/deleteall', methods=['DELETE'])
def delete_all_file():
    dir_name = app.config["UPLOAD_FOLDER"]
    for name in os.listdir(dir_name):
        os.remove(os.path.join(dir_name, name))
    return jsonify({"success": True})

@app.route('/links')
def get_links():
    dir_name = app.config["UPLOAD_FOLDER"]
    list_of_files = filter(lambda x: os.path.isfile(os.path.join(dir_name, x)),
                           os.listdir(dir_name))
    list_of_files = sorted(list_of_files,
                           key=lambda x: os.path.getmtime(os.path.join(dir_name, x)), reverse=True)
    return jsonify([(request.url_root + 'docs/' + filename) for filename in list_of_files])


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        print(request.files)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return request.url_root + 'docs/' + file.filename
            # return redirect(url_for('download_file', name=filename))
    return render_template('uploadform.html')
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
