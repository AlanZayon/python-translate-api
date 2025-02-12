from flask import Flask, request, jsonify,send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from utils.extract_text import extract_text_with_positions
from utils.translate import translate_texts
from utils.generate_pdf import replace_text_in_pdf

app = Flask(__name__)
CORS(app)
CORS(app, origins=["http://localhost:5173"])

UPLOAD_FOLDER = 'uploads/'
TRANSLATED_FOLDER = 'translated/'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TRANSLATED_FOLDER'] = TRANSLATED_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    print("📩 Recebendo requisição de upload...")
    print("📦 request.files:", request.files)
    print("📨 request.form:", request.form)

    if 'file' not in request.files:
        print("'error': 'No file part'")
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        print("'error': 'No selected file'")
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_pdf = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_pdf)

        output_pdf = os.path.join(app.config['TRANSLATED_FOLDER'], 'translated_file.pdf')

        # Processo de extração, tradução e substituição
        extracted_data = extract_text_with_positions(input_pdf)
        translated_data = translate_texts(extracted_data, 'pt')
        replace_text_in_pdf(input_pdf, translated_data, output_pdf)

        # 🔥 Remove o arquivo original após a tradução
        try:
            os.remove(input_pdf)
            print(f"🗑️ Arquivo removido: {input_pdf}")
        except Exception as e:
            print(f"⚠️ Erro ao remover arquivo: {e}")

        return jsonify({'download_url': f'/download/{os.path.basename(output_pdf)}'}), 200


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['TRANSLATED_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
