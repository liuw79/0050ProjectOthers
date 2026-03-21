#!/usr/bin/env python3

try:
    import PyPDF2
    
    with open('/Users/liuwei/SynologyDrive/0050Project/Ceo.Ceo/03_组织与团队/高维学堂2025年成果复盘会.pdf', 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + '\n'
        print(text)
except ImportError:
    print('PyPDF2 not installed, trying alternative method...')
    try:
        import fitz  # PyMuPDF
        doc = fitz.open('/Users/liuwei/SynologyDrive/0050Project/Ceo.Ceo/03_组织与团队/高维学堂2025年成果复盘会.pdf')
        text = ''
        for page in doc:
            text += page.get_text() + '\n'
        print(text)
        doc.close()
    except ImportError:
        print('Neither PyPDF2 nor PyMuPDF is installed')
        print('PDF content extraction requires additional libraries')
except Exception as e:
    print(f'Error reading PDF: {e}')