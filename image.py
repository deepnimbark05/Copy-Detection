from PIL import Image
import fitz  # PyMuPDF

# Function to merge images
def merge_images(images):
    if not images:
        return None

    # Determine the output image size (use the size of the first image)
    first_image = images[0]
    width, height = first_image.width, first_image.height

    # Create a new blank image
    merged_image = Image.new('RGB', (width, len(images) * height))

    # Paste each image into the merged image
    for i, image in enumerate(images):
        merged_image.paste(image, (0, i * height))

    return merged_image

# Collect PDF images
pdf_images = []
pdf_document_path = input("Enter the path to the PDF file: ")
pdf_document = fitz.open(pdf_document_path)

for page_number in range(pdf_document.page_count):
    page = pdf_document.load_page(page_number)
    images = page.get_pixmap()

    pdf_images.append(Image.frombytes("RGB", [images.width, images.height], images.samples))

pdf_document.close()

# Merge the PDF images
merged_pdf_image = merge_images(pdf_images)

if merged_pdf_image:
    merged_pdf_image.show()
else:
    print("No images found in the PDF or unable to merge.")

# You can also save the merged image to a file if needed
# merged_pdf_image.save("merged_image.png")
