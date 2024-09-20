from PIL import Image
from skimage import color, transform
from skimage.metrics import structural_similarity as compare_ssim
import fitz  # PyMuPDF
import io
import tempfile
import cv2
from fpdf import FPDF
import os
import webbrowser

def compare_images(image1_path, image2_path):
    """Compare two images and return their Structural Similarity Index (SSIM)."""
    image1_cv = cv2.imread(image1_path)
    image2_cv = cv2.imread(image2_path)

    # Resize image2 to match the dimensions of image1
    image2_cv = transform.resize(image2_cv, image1_cv.shape, mode='reflect', anti_aliasing=True)

    # Convert images to grayscale
    image1_gray = color.rgb2gray(image1_cv)
    image2_gray = color.rgb2gray(image2_cv)

    # Compute SSIM between the two grayscale images
    ssim, _ = compare_ssim(image1_gray, image2_gray, full=True, data_range=image2_gray.max() - image2_gray.min())

    return ssim

def extract_images_from_pdf(pdf_document):
    """Extract images from a PDF and return a list of image file paths."""
    images_list = []

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
                images_list.append(temp_image_path)

    return images_list

def create_merged_pdf(output_pdf_name, images_pdf1, images_pdf2, threshold=0.8):
    """Compare images from two PDFs, merge similar images, and create a new merged PDF."""
    merged_pdf = FPDF()
    similar_pages_found = False

    # Loop through all images from PDF1 and compare each with every image in PDF2
    for i, image_pdf1_path in enumerate(images_pdf1):
        for j, image_pdf2_path in enumerate(images_pdf2):
            similarity = compare_images(image_pdf1_path, image_pdf2_path)

            if similarity >= threshold:
                similar_pages_found = True  # Flag when similar pages are found
                print(f"Merging image from PDF1 page {i + 1} with PDF2 page {j + 1} (Similarity: {similarity:.2f})")

                image_pdf1 = Image.open(image_pdf1_path)
                image_pdf2 = Image.open(image_pdf2_path)

                # Resize image2 to match image1 if necessary
                if image_pdf1.size != image_pdf2.size:
                    image_pdf2 = image_pdf2.resize(image_pdf1.size)

                # Convert both images to RGB to ensure compatibility
                image_pdf1 = image_pdf1.convert("RGB")
                image_pdf2 = image_pdf2.convert("RGB")

                # Blend the images with a 50% alpha blend
                merged_image = Image.blend(image_pdf1, image_pdf2, alpha=0.5)

                # Save the merged image to a temporary file
                with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_image_file:
                    merged_image_path = temp_image_file.name
                    merged_image.save(merged_image_path)

                # Add a new page and place the merged image in the PDF
                merged_pdf.add_page()
                merged_pdf.image(merged_image_path, x=10, y=10, w=190)  # Adjust width to fit within margins

    # Check if any similar pages were found and save the merged PDF
    if similar_pages_found:
        merged_pdf.output(output_pdf_name)
        print(f"Merged PDF saved as {output_pdf_name}")
        return True
    else:
        print("No similar pages found, PDF was not created.")
        return False

def main():
    # Define the base directory where the PDF files are located
    base_directory = "D:/study/Copy Detection/pdf/"

    # Get input file names from the user
    pdf_document1_name = input("Enter the name of the first PDF file (e.g., last.pdf): ")
    pdf_document2_name = input("Enter the name of the second PDF file (e.g., reali.pdf): ")

    # Concatenate the base directory with the user-provided file names
    pdf_document1_path = os.path.join(base_directory, pdf_document1_name)
    pdf_document2_path = os.path.join(base_directory, pdf_document2_name)

    # Show the full input paths for the PDFs
    print(f"First PDF path: {pdf_document1_path}")
    print(f"Second PDF path: {pdf_document2_path}")

    # Open the two PDF documents
    pdf_document1 = fitz.open(pdf_document1_path)
    pdf_document2 = fitz.open(pdf_document2_path)

    # Get the desired output PDF name from the user
    output_pdf_name = input("Enter the desired name for the output PDF (without extension): ") + ".pdf"
    output_pdf_path = os.path.join(base_directory, output_pdf_name)

    # Extract images from both PDFs
    images_pdf1 = extract_images_from_pdf(pdf_document1)
    images_pdf2 = extract_images_from_pdf(pdf_document2)

    # Close the original PDFs
    pdf_document1.close()
    pdf_document2.close()

    # Create the merged PDF if similar pages are found
    if create_merged_pdf(output_pdf_path, images_pdf1, images_pdf2):
        # Automatically open the merged PDF after saving
        webbrowser.open(f"file://{os.path.abspath(output_pdf_path)}")

if __name__ == "__main__":
    main()
