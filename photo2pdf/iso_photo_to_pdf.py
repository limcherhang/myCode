from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
import os

def resize_image(input_path, output_path, quality=85):
    img = Image.open(input_path)
    img.save(output_path, 'JPEG', quality=quality)

def get_all_files_in_directory(directory_path):
    # 获取目录下的所有文件和子目录
    all_files = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            # 得到文件的绝对路径
            file_path = os.path.join(root, file)
            all_files.append(file_path)

    return all_files

def images_to_pdf(image_paths, output_pdf):
    # Create a new PDF document
    pdf_canvas = canvas.Canvas(output_pdf, pagesize=letter)

    # Iterate through each image and add it to the PDF
    for image_path in image_paths:
        # Open the image using Pillow
        img = resize_image(image_path, image_path)
        img = Image.open(image_path)


        # Get the dimensions of the image
        width, height = img.size

        # Add a new page to the PDF with the dimensions of the image
        pdf_canvas.setPageSize((width, height))
        pdf_canvas.showPage()

        # Draw the image on the PDF
        pdf_canvas.drawInlineImage(img, 0, 0, width, height)

    # Save the PDF
    pdf_canvas.save()

if __name__ == "__main__":
    # List of image paths in the desired order
    path = 'images'
    image_paths = get_all_files_in_directory(path)

    # Output PDF file
    output_pdf = "output.pdf"

    # Convert images to PDF
    images_to_pdf(image_paths, output_pdf)

    print(f"PDF generated successfully: {output_pdf}")