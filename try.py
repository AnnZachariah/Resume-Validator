import pdf2image

pdf_file_path = r"C:\Users\annza\OneDrive\Desktop\Resume\Ann Elizabeth Zachariah Resume.pdf"
poppler_path = r"C:\Users\annza\Documents\tp wks\ATS\poppler-24.08.0\Library\bin"

try:
    images = pdf2image.convert_from_path(pdf_file_path, poppler_path=poppler_path)
    print(f"Successfully converted {len(images)} pages.")
except Exception as e:
    print(f"Error: {e}")
