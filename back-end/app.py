from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from pdf2tex import convert_pdf_to_tex

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'})

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file format'})

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    tex_code = convert_pdf_to_tex(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return jsonify({'tex_code': tex_code})

if __name__ == '__main__':
    app.run()
