from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import io
import os
import logging
from logging.handlers import RotatingFileHandler
from gabungkan import gabungkan_pdf
from resize import resize_pdf
import traceback

app = Flask(__name__)
CORS(app)

# Konfigurasi logging
if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Application startup')

@app.route('/api/gabung_pdf', methods=['POST'])
def gabungkan_pdf_api():
    try:
        app.logger.info('Received request to merge PDFs')
        pdf_files = request.files.getlist('pdfs')
        if not pdf_files:
            app.logger.warning('No PDF files provided in the request')
            return jsonify({"error": "No PDF files provided"}), 400
        output = gabungkan_pdf(pdf_files)
        app.logger.info('PDFs merged successfully')
        return send_file(output, as_attachment=True, download_name='gabungan.pdf', mimetype='application/pdf')
    except Exception as e:
        app.logger.error(f"Error in gabungkan_pdf_api: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({"error": "An internal error occurred. Please check the logs for more details."}), 500

@app.route('/api/resize_pdf', methods=['POST'])
def resize_pdf_api():
    try:
        app.logger.info('Received request to resize PDF')
        if 'pdf' not in request.files:
            app.logger.warning('No PDF file provided in the request')
            return jsonify({"error": "No PDF file provided"}), 400
        pdf_file = request.files['pdf']
        scale_factor = float(request.form.get('scale_factor', 1.0))
        app.logger.info(f'Resizing PDF with scale factor: {scale_factor}')
        resized_pdf = resize_pdf(pdf_file, scale_factor)
        app.logger.info('PDF resized successfully')
        return send_file(resized_pdf, as_attachment=True, download_name='resized.pdf', mimetype='application/pdf')
    except ValueError as ve:
        app.logger.error(f"ValueError in resize_pdf_api: {str(ve)}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        app.logger.error(f"Error in resize_pdf_api: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({"error": "An internal error occurred. Please check the logs for more details."}), 500

if __name__ == '__main__':
    app.run(debug=True)