from flask import Flask, send_from_directory, request, jsonify
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'data'  # Pasta para armazenar o CSV
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Cria a pasta se não existir

@app.route('/download_csv')
def download_csv():
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'data.csv', as_attachment=True)

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'data.csv'))
    return jsonify({'message': 'File uploaded successfully'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)