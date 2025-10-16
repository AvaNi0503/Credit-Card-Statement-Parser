# Create a simple test script to demonstrate PDF processing
test_script = '''#!/usr/bin/env python3
"""
Test Script for PDF Credit Card Statement Parser
Demonstrates how to use the enhanced parser with PDF files

Usage: python test_pdf_parser.py [pdf_file_path]
"""

import sys
import os
import json
from enhanced_pdf_parser import EnhancedCreditCardParser

def test_parser():
    """Test the PDF parser with various scenarios"""
    parser = EnhancedCreditCardParser()
    
    print("="*60)
    print("🧪 PDF Credit Card Statement Parser Test")
    print("="*60)
    
    # Check if a specific file was provided
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        
        if not os.path.exists(pdf_path):
            print(f"❌ Error: File '{pdf_path}' not found")
            return
        
        print(f"📄 Testing with: {pdf_path}")
        print("-" * 40)
        
        result = parser.parse_pdf_statement(pdf_path)
        display_result(result)
        
    else:
        # Look for sample PDFs in current directory
        pdf_files = [f for f in os.listdir('.') if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            print("📝 No PDF files found in current directory.")
            print("\\n💡 To test the parser:")
            print("1. Place a credit card statement PDF in this folder")
            print("2. Run: python test_pdf_parser.py your_statement.pdf")
            print("\\n🏦 Supported banks: HDFC, ICICI, SBI, Axis Bank, Kotak Mahindra")
            demonstrate_text_parsing()
            return
        
        print(f"📁 Found {len(pdf_files)} PDF file(s) to test:")
        for i, pdf_file in enumerate(pdf_files, 1):
            print(f"{i}. {pdf_file}")
        
        print("\\n" + "="*60)
        
        # Test each PDF
        for pdf_file in pdf_files[:3]:  # Limit to first 3 PDFs
            print(f"\\n📄 Processing: {pdf_file}")
            print("-" * 40)
            
            result = parser.parse_pdf_statement(pdf_file)
            display_result(result)
            
            if len(pdf_files) > 1:
                input("\\nPress Enter to continue to next file...")

def display_result(result):
    """Display parsing results in a formatted way"""
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        
        if 'supported_banks' in result:
            print(f"\\n🏦 Supported banks: {', '.join(result['supported_banks'])}")
        
        if 'extracted_text_preview' in result:
            print(f"\\n📝 Text preview (first 200 chars):")
            print(f"'{result['extracted_text_preview'][:200]}...'")
            
    else:
        print("✅ Successfully extracted data!")
        print("\\n📊 Results:")
        print(f"  🏦 Bank: {result['bank']}")
        print(f"  💳 Account: {result['account_number']}")  
        print(f"  📅 Period: {result['statement_period']}")
        print(f"  💰 Balance: ₹{result['total_balance']}")
        print(f"  ⏰ Due Date: {result['payment_due_date']}")
        print(f"  💳 Credit Limit: ₹{result['credit_limit']}")
        print(f"  📄 Source: {result.get('source_file', 'N/A')}")
        print(f"  📏 File Size: {result.get('file_size', 'N/A')} bytes")
        print(f"  🔧 Method: {result.get('extraction_method', 'N/A')}")
        print(f"  ⏱️ Parsed: {result.get('parsed_at', 'N/A')}")
        
        # Validation check
        missing_fields = [field for field, value in result.items() 
                         if value == 'Not found' and field in 
                         ['account_number', 'total_balance', 'payment_due_date', 
                          'credit_limit', 'statement_period']]
        
        if missing_fields:
            print(f"\\n⚠️ Missing fields: {', '.join(missing_fields)}")
        else:
            print("\\n🎯 All required fields extracted successfully!")

def demonstrate_text_parsing():
    """Show how the parser works with sample text"""
    parser = EnhancedCreditCardParser()
    
    print("\\n" + "="*50)
    print("📝 Demonstrating with sample text...")
    print("="*50)
    
    sample_text = """
    HDFC Bank Credit Card Statement
    Card Number: ****1234
    Statement Period: 01-Sep-2024 to 30-Sep-2024
    Total Amount Due: ₹45,230.50
    Payment Due Date: 25-10-2024
    Credit Limit: ₹200000
    """
    
    print("Sample HDFC statement text:")
    print(sample_text)
    
    result = parser.parse_text_statement(sample_text)
    print("\\nParsing result:")
    display_result(result)

if __name__ == "__main__":
    try:
        test_parser()
    except KeyboardInterrupt:
        print("\\n\\n👋 Test interrupted by user")
    except Exception as e:
        print(f"\\n❌ Unexpected error: {e}")
        print("\\n💡 Make sure you have installed the required libraries:")
        print("pip install PyPDF2 pdfplumber")
'''

# Save test script
with open('test_pdf_parser.py', 'w', encoding='utf-8') as f:
    f.write(test_script)

# Make the script executable
os.chmod('test_pdf_parser.py', 0o755)

print("✓ Created test_pdf_parser.py (executable)")
print("\nTest script features:")
print("- Command line interface")
print("- Automatic PDF detection")
print("- Formatted result display") 
print("- Error handling and validation")
print("- Sample text demonstration")
print("\nUsage: python test_pdf_parser.py [pdf_file]")