from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    options = ['Option 1', 'Option 2', 'Option 3']
    return render_template('index.html', options=options)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    # You can save the file or perform any action here
    return "File uploaded successfully"

if __name__ == '__main__':
    app.run(debug=True)
