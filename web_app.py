from flask import Flask, request, jsonify, render_template # Import render_template
from readers import csv_reader, xlsx_reader
from services import document_identifier
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/') # Add a route for the root URL '/'
def index():
    """
    Serves the index.html page for file upload UI.
    """
    return render_template('index.html') # Flask will look for index.html in the 'templates' folder by default


@app.route('/upload', methods=['POST'])
def upload_file():
    # ... (rest of your upload_file() function code remains exactly the same as before) ...
    # ... (no changes needed in upload_file() for this step) ...


if __name__ == '__main__':
    app.run(debug=True)