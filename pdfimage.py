import fitz
from PIL import Image
import io

pdf_document_path = input("Enter the path to the PDF file: ")
pdf_document = fitz.open(pdf_document_path)

image_list = []

for page_number in range(pdf_document.page_count):
    page = pdf_document.load_page(page_number)

    images = page.get_images(full=True)

    for img_index, img in enumerate(images):
        xref = img[0]
        base_image = pdf_document.extract_image(xref)
        image_data = base_image["image"]
        image_format = base_image["ext"]

        pil_image = Image.open(io.BytesIO(image_data))
        image_list.append(pil_image)

pdf_document.close()

# Save the images as PNG files and display them
for i, image in enumerate(image_list):
    image.save(f'image_{i}.png')
    image.show()

# Optional: You can also specify the image file format when saving, e.g., image.save(f'image_{i}.jpg', 'JPEG')
