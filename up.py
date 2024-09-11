
import fitz
from PIL import Image
import io

pdf_document = input("Enter the path to the PDF file: ")
pdf_document = fitz.open(pdf_document)
pdf_image = Image.open('sreen.jpg')

# Create a list to store merged images
image2 = []

for page_number in range(pdf_document.page_count):
    page = pdf_document.load_page(page_number)

    images = page.get_images(full=True)

    for img_index, img in enumerate(images):
        xref = img[0]
        base_image = pdf_document.extract_image(xref)
        image_data = base_image["image"]
        image_format = base_image["ext"]

        pil_image = Image.open(io.BytesIO(image_data))

        # Resize the PDF image to match the size of the given image
        pdf_image_resized = pdf_image.resize(pil_image.size)

        # Overlay the PDF image on top of the given image
        merged_image = Image.blend(pil_image, pdf_image_resized, alpha=0.5)  # Adjust the alpha value as needed

        # Append the merged image to the list
        image2.append(merged_image)

# Merge all the images into one
    merged_image = image2[0]
    for i in range(0, len(image2)):
        merged_image = Image.blend(merged_image, image2[i], alpha=1.0)
        merged_image.show()

    pdf_document.close()
