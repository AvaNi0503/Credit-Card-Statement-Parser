# Create an enhanced version that can handle PDF files
enhanced_parser_code = '''"""
Enhanced Credit Card Statement Parser with PDF Support
Now accepts PDF files directly and extracts text automatically

Requirements:
pip install PyPDF2 pdfplumber

This parser extracts 5 key data points from PDF credit card statements:
1. Account Number (last 4 digits)
2. Statement Period  
3. Total Balance
4. Payment Due Date
5. Credit Limit

Supports: HDFC, ICICI, SBI, Axis Bank, Kotak Mahindra
"""

import re
import json
import os
from datetime import datetime

# PDF processing imports
try:
    import PyPDF2
    import pdfplumber
    PDF_SUPPORT = True
except ImportError:
    print("WARNING: PDF libraries not installed.")
    print("Install with: pip install PyPDF2 pdfplumber")
    PDF_SUPPORT = False

class EnhancedCreditCardParser:
    def __init__(self):
        # Bank patterns for text extraction
        self.bank_patterns = {
            'HDFC': {
                'account_pattern': r'(?:Card Number|Card No\\.?).*?(\\*{4}\\d{4})',
                'balance_pattern': r'(?:Total Amount Due|Amount Due|Outstanding).*?₹?\\s*([\\d,]+\\.?\\d*)',
                'due_date_pattern': r'(?:Payment Due Date|Due Date).*?(\\d{1,2}[-/]\\d{1,2}[-/]\\d{4})',
                'credit_limit_pattern': r'(?:Credit Limit|Available Limit).*?₹?\\s*([\\d,]+)',
                'statement_period_pattern': r'(?:Statement Period|Bill Period).*?(\\d{1,2}[-/]\\w{3}[-/]\\d{4})\\s*(?:to|-)\\s*(\\d{1,2}[-/]\\w{3}[-/]\\d{4})'
            },
            'ICICI': {
                'account_pattern': r'(?:Card No\\.?|Card Number).*?(\\*{4}\\d{4})',
                'balance_pattern': r'(?:Outstanding Amount|Total Due|Amount Due).*?Rs\\.?\\s*([\\d,]+\\.?\\d*)',
                'due_date_pattern': r'(?:Due Date|Payment Date).*?(\\d{1,2}[/-]\\d{1,2}[/-]\\d{4})',
                'credit_limit_pattern': r'(?:Available Credit Limit|Credit Limit).*?Rs\\.?\\s*([\\d,]+)',
                'statement_period_pattern': r'(?:Bill Period|Statement Period).*?(\\d{1,2}[/-]\\d{1,2}[/-]\\d{4})\\s*(?:to|-)\\s*(\\d{1,2}[/-]\\d{1,2}[/-]\\d{4})'
            },
            'SBI': {
                'account_pattern': r'(?:Credit Card Number|Card No).*?(\\*{4}\\d{4})',
                'balance_pattern': r'(?:Total Amount Payable|Outstanding|Total Due).*?Rs\\.?\\s*([\\d,]+\\.?\\d*)',
                'due_date_pattern': r'(?:Payment Due By|Due Date).*?(\\d{1,2}[-]\\d{1,2}[-]\\d{4})',
                'credit_limit_pattern': r'(?:Total Credit Limit|Credit Limit).*?Rs\\.?\\s*([\\d,]+)',
                'statement_period_pattern': r'(?:Statement Date|Bill Period).*?(\\d{1,2}[-]\\d{1,2}[-]\\d{4})\\s*(?:to|-)\\s*(\\d{1,2}[-]\\d{1,2}[-]\\d{4})'
            },
            'AXIS': {
                'account_pattern': r'(?:Card Number|Card No).*?(\\*{4}\\d{4})',
                'balance_pattern': r'(?:Amount Due|Total Outstanding).*?Rs\\.?\\s*([\\d,]+\\.?\\d*)',
                'due_date_pattern': r'(?:Due Date|Payment Date).*?(\\d{1,2}[/]\\d{1,2}[/]\\d{4})',
                'credit_limit_pattern': r'(?:Credit Limit|Available Limit).*?Rs\\.?\\s*([\\d,]+)',
                'statement_period_pattern': r'(?:Statement Period|Bill Date).*?(\\d{1,2}[/]\\d{1,2}[/]\\d{4})\\s*(?:to|-)\\s*(\\d{1,2}[/]\\d{1,2}[/]\\d{4})'
            },
            'KOTAK': {
                'account_pattern': r'(?:Card No|Card Number).*?(\\*{4}\\d{4})',
                'balance_pattern': r'(?:Total Outstanding|Amount Due).*?₹\\s*([\\d,]+\\.?\\d*)',
                'due_date_pattern': r'(?:Payment Due|Due Date).*?(\\d{1,2}[-]\\w{3}[-]\\d{4})',
                'credit_limit_pattern': r'(?:Credit Limit|Available Credit).*?₹\\s*([\\d,]+)',
                'statement_period_pattern': r'(?:Bill Date|Statement Period).*?(\\d{1,2}[-]\\w{3}[-]\\d{4})\\s*(?:to|-)\\s*(\\d{1,2}[-]\\w{3}[-]\\d{4})'
            }
        }
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF using multiple methods for better accuracy"""
        if not PDF_SUPPORT:
            raise ImportError("PDF libraries not installed. Run: pip install PyPDF2 pdfplumber")
        
        text = ""
        
        # Method 1: Try pdfplumber first (better for tables and formatted text)
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\\n"
            print(f"✓ Extracted text using pdfplumber ({len(text)} characters)")
        except Exception as e:
            print(f"pdfplumber failed: {e}")
            
        # Method 2: Fallback to PyPDF2 if pdfplumber fails or returns little text
        if len(text.strip()) < 100:
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\\n"
                print(f"✓ Extracted text using PyPDF2 ({len(text)} characters)")
            except Exception as e:
                print(f"PyPDF2 also failed: {e}")
                return None
                
        return text.strip() if text.strip() else None
    
    def detect_bank(self, text):
        """Identify which bank issued the statement"""
        text_lower = text.lower()
        
        # Look for bank identifiers
        if any(keyword in text_lower for keyword in ['hdfc', 'housing development finance']):
            return 'HDFC'
        elif any(keyword in text_lower for keyword in ['icici', 'industrial credit']):
            return 'ICICI'
        elif any(keyword in text_lower for keyword in ['sbi', 'state bank of india', 'sbi card']):
            return 'SBI'
        elif any(keyword in text_lower for keyword in ['axis', 'axis bank']):
            return 'AXIS'
        elif any(keyword in text_lower for keyword in ['kotak', 'kotak mahindra']):
            return 'KOTAK'
        else:
            return None
    
    def clean_extracted_value(self, value):
        """Clean and format extracted values"""
        if not value:
            return 'Not found'
        
        # Remove extra whitespace and clean up
        value = re.sub(r'\\s+', ' ', value.strip())
        
        # Remove currency symbols for amounts
        value = re.sub(r'[₹Rs\\.]', '', value)
        
        return value
    
    def extract_data_from_text(self, text, bank):
        """Extract the 5 required fields from statement text"""
        if bank not in self.bank_patterns:
            return None
        
        patterns = self.bank_patterns[bank]
        data = {}
        
        # Extract each field with improved regex
        try:
            # Account Number
            account_match = re.search(patterns['account_pattern'], text, re.IGNORECASE | re.DOTALL)
            data['account_number'] = self.clean_extracted_value(account_match.group(1) if account_match else None)
            
            # Total Balance
            balance_match = re.search(patterns['balance_pattern'], text, re.IGNORECASE | re.DOTALL)
            data['total_balance'] = self.clean_extracted_value(balance_match.group(1) if balance_match else None)
            
            # Payment Due Date
            due_date_match = re.search(patterns['due_date_pattern'], text, re.IGNORECASE | re.DOTALL)
            data['payment_due_date'] = self.clean_extracted_value(due_date_match.group(1) if due_date_match else None)
            
            # Credit Limit
            credit_limit_match = re.search(patterns['credit_limit_pattern'], text, re.IGNORECASE | re.DOTALL)
            data['credit_limit'] = self.clean_extracted_value(credit_limit_match.group(1) if credit_limit_match else None)
            
            # Statement Period
            period_match = re.search(patterns['statement_period_pattern'], text, re.IGNORECASE | re.DOTALL)
            if period_match:
                data['statement_period'] = f"{period_match.group(1)} to {period_match.group(2)}"
            else:
                data['statement_period'] = 'Not found'
            
        except Exception as e:
            print(f"Error extracting data: {e}")
            return None
        
        # Add metadata
        data['bank'] = bank
        data['parsed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data['extraction_method'] = 'PDF'
        
        return data
    
    def parse_pdf_statement(self, pdf_path):
        """Main method to parse PDF credit card statement"""
        # Validate file
        if not os.path.exists(pdf_path):
            return {'error': f'File not found: {pdf_path}'}
        
        if not pdf_path.lower().endswith('.pdf'):
            return {'error': 'File must be a PDF'}
        
        print(f"📄 Processing PDF: {pdf_path}")
        
        # Step 1: Extract text from PDF
        text = self.extract_text_from_pdf(pdf_path)
        
        if not text:
            return {'error': 'Could not extract text from PDF. PDF might be image-based or corrupted.'}
        
        print(f"📝 Extracted {len(text)} characters of text")
        
        # Step 2: Detect bank
        bank = self.detect_bank(text)
        
        if not bank:
            return {
                'error': 'Could not identify bank from PDF',
                'supported_banks': list(self.bank_patterns.keys()),
                'extracted_text_preview': text[:500] + '...' if len(text) > 500 else text
            }
        
        print(f"🏦 Detected bank: {bank}")
        
        # Step 3: Extract data
        extracted_data = self.extract_data_from_text(text, bank)
        
        if not extracted_data:
            return {'error': 'Failed to extract data from PDF text'}
        
        # Step 4: Add file information
        extracted_data['source_file'] = os.path.basename(pdf_path)
        extracted_data['file_size'] = os.path.getsize(pdf_path)
        
        return extracted_data
    
    def parse_text_statement(self, text):
        """Parse statement from plain text (backward compatibility)"""
        bank = self.detect_bank(text)
        
        if not bank:
            return {
                'error': 'Could not identify bank from text',
                'supported_banks': list(self.bank_patterns.keys())
            }
        
        data = self.extract_data_from_text(text, bank)
        if data:
            data['extraction_method'] = 'Text'
        
        return data

def batch_process_pdfs(folder_path):
    """Process multiple PDF files in a folder"""
    parser = EnhancedCreditCardParser()
    results = []
    
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return
    
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"No PDF files found in {folder_path}")
        return
    
    print(f"Found {len(pdf_files)} PDF files to process...")
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        print(f"\\n{'='*50}")
        print(f"Processing: {pdf_file}")
        print('='*50)
        
        result = parser.parse_pdf_statement(pdf_path)
        results.append({
            'file': pdf_file,
            'result': result
        })
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✅ Successfully parsed {result['bank']} statement")
    
    # Save results
    output_file = os.path.join(folder_path, 'parsing_results.json')
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\\n📊 Results saved to: {output_file}")
    return results

def demo_with_pdf():
    """Demo function for PDF parsing"""
    parser = EnhancedCreditCardParser()
    
    print("=== PDF Credit Card Statement Parser Demo ===\\n")
    
    # Check if sample PDF exists
    sample_pdf = "sample_statement.pdf"
    
    if os.path.exists(sample_pdf):
        print("Processing sample PDF...")
        result = parser.parse_pdf_statement(sample_pdf)
        print(json.dumps(result, indent=2))
    else:
        print(f"No sample PDF found. Place a credit card statement PDF as '{sample_pdf}' to test.")
        print("\\nOr use the parser like this:")
        print("""
parser = EnhancedCreditCardParser()
result = parser.parse_pdf_statement('your_statement.pdf')
print(json.dumps(result, indent=2))
        """)

if __name__ == "__main__":
    if not PDF_SUPPORT:
        print("Please install PDF processing libraries first:")
        print("pip install PyPDF2 pdfplumber")
        exit(1)
    
    demo_with_pdf()
'''

# Save the enhanced parser
with open('enhanced_pdf_parser.py', 'w', encoding='utf-8') as f:
    f.write(enhanced_parser_code)

print("✓ Created enhanced_pdf_parser.py with PDF support")
print("\nNew features:")
print("- Direct PDF file processing")
print("- Multiple extraction methods (pdfplumber + PyPDF2)")
print("- Batch processing capability")
print("- Better error handling")
print("- File metadata extraction")