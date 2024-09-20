
from PIL import Image
from skimage import color, transform
from skimage.metrics import structural_similarity as compare_ssim
from tkinter import simpledialog
import pyautogui
import fitz
import io
import cv2
import tempfile

pdf_document_path = input("Enter the path to the PDF file: ")
pdf_document = fitz.open(pdf_document_path)

def compare_images(image1, image2):
    image1_path = cv2.imread(image1)
    image2_path = cv2.imread(image2)

    image2_path = transform.resize(image2_path, image1_path.shape, mode='reflect', anti_aliasing=True)

    image1_gray = color.rgb2gray(image1_path)
    image2_gray = color.rgb2gray(image2_path)

    ssim = compare_ssim(image1_gray, image2_gray, data_range=image2_gray.max() - image2_gray.min())

    return ssim

# List of image filenames
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

        # Create a temporary image file
        with tempfile.NamedTemporaryFile(suffix=f".{image_format}", delete=False) as temp_image_file:
            temp_image_path = temp_image_file.name
            pil_image.save(temp_image_path)
            image2.append(temp_image_path)

# Capture a screenshot
screenshot = pyautogui.screenshot()
file_name = simpledialog.askstring("Input", "Enter the file name to save the screenshot:")

if file_name:
    screenshot.save(f"{file_name}.png")
    print(f"Screenshot saved as {file_name}.png")

    threshold = 0.7


    for i in range(0,len(image2)):
        similarity = compare_images(f"{file_name}.png", image2[i])

        if similarity >= threshold:
            print(f"Merging screenshot with page {i + 1} (Similarity: {similarity:.2f})")
            image3 = Image.open(f"{file_name}.png")
            image4 = Image.open(image2[i])

            if image3.size != image4.size:
                image4 = image4.resize(image3.size)

            image3 = image3.convert("RGB")
            image4 = image4.convert("RGB")

            merged_image = Image.blend(image3, image4, alpha=0.5)

            merged_image.show()

    pdf_document.close()
else:
    print("No file name provided. Screenshot not saved.")

