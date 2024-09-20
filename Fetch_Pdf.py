import fitz  # PyMuPDF
import io
from PIL import Image

# Get PDF document path from user
pdf_document_path = input("Enter the path to the PDF file: ")
pdf_document = fitz.open(pdf_document_path)

# List to store images of each page
page_images = []

# Iterate through each page in the PDF
for page_number in range(pdf_document.page_count):
    page = pdf_document.load_page(page_number)

    # Render the page to an image (pixmap)
    pix = page.get_pixmap()

    # Convert the pixmap to a PIL image
    pil_image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    page_images.append(pil_image)

# Combine all page images into one
combined_width = max(image.width for image in page_images)
combined_height = sum(image.height for image in page_images)

# Create a new image with the combined dimensions
combined_image = Image.new('RGB', (combined_width, combined_height))

# Paste each page image into the combined image
y_offset = 0
for image in page_images:
    combined_image.paste(image, (0, y_offset))
    y_offset += image.height

# Show the combined image
combined_image.show(title="Combined PDF Pages")

# Close the PDF document
pdf_document.close()
