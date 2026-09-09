from matplotlib import image
import pypdf

def is_pdf_with_images(pdf_path):
    with open(pdf_path, "rb") as f:
        pdf_reader = pypdf.PdfReader(f)
        for page in pdf_reader.pages:
            if page.images:
                return True
    return False

def extract_images_from_pdf(pdf_path):
    image_data = []
    with open(pdf_path, "rb") as f:
        pdf_reader = pypdf.PdfReader(f)
        for page in pdf_reader.pages:
            for image_obj in page.images:
                image_data.append(image_obj.data)
    return image_data if image_data else None

def ocr_image(image_data):
    # Placeholder for OCR implementation
    # You can use libraries like pytesseract or easyocr for actual OCR processing
    return "Extracted text from image"

def extract_text_from_pdf(pdf_path):
    text_data = []
    with open(pdf_path, "rb") as f:
        pdf_reader = pypdf.PdfReader(f)
        for page in pdf_reader.pages:
            text_data.append(page.extract_text())
    return "\n".join(text_data) if text_data else None

def merge_text_and_images(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    images = extract_images_from_pdf(pdf_path)
    
    if images:
        ocr_texts = [ocr_image(image) for image in images]
        combined_text = text + "\n" + "\n".join(ocr_texts) if text else "\n".join(ocr_texts)
        return combined_text
    return text

def normalize_text(text):
    return text.lower().strip().replace("\n", " ") if text else ""












if __name__ == "__main__":
    pdf_path = ""
    if is_pdf_with_images(pdf_path):
        combined_text = merge_text_and_images(pdf_path)
        normalized_text = normalize_text(combined_text)
        print(normalized_text)
    else:
        text = extract_text_from_pdf(pdf_path)
        normalized_text = normalize_text(text)
        print(normalized_text)