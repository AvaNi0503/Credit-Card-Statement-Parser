# Create a Flask web application that can handle PDF uploads and processing
flask_app_code = '''"""
Flask Web Application for PDF Credit Card Statement Parser
Provides a complete web interface with backend processing

Requirements:
pip install Flask PyPDF2 pdfplumber

Run with: python flask_pdf_parser.py
"""

from flask import Flask, request, render_template, jsonify, send_from_directory
import os
import json
from werkzeug.utils import secure_filename
from enhanced_pdf_parser import EnhancedCreditCardParser

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads directory
os.makedirs('uploads', exist_ok=True)

# Initialize parser
parser = EnhancedCreditCardParser()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file selected'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the PDF
        result = parser.parse_pdf_statement(filepath)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'supported_banks': list(parser.bank_patterns.keys())
    })

if __name__ == '__main__':
    print("Starting PDF Credit Card Statement Parser Web App...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
'''

# Save Flask application
with open('flask_pdf_parser.py', 'w', encoding='utf-8') as f:
    f.write(flask_app_code)

print("✓ Created flask_pdf_parser.py")
print("\nFlask Web App features:")
print("- Complete backend API")
print("- File upload handling")
print("- PDF processing endpoint")
print("- Error handling")
print("- Automatic file cleanup")