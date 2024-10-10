# src/services/pdf_processor.py

import fitz  # PyMuPDF
from typing import List
from src.models.page_content import PageContent

class PDFProcessor:
    def __init__(self):
        pass

    def process_pdf(self, pdf_path: str, text_only: bool = False) -> List[PageContent]:
        doc = fitz.open(pdf_path)
        pages_content = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            images = page.get_images()

            if images and not text_only:
                # Page contains images
                # Get original page size
                rect = page.rect
                width, height = rect.width, rect.height

                # Determine the scaling factor
                if width < height:
                    scale = 500 / width
                else:
                    scale = 500 / height

                # Create a transformation matrix for scaling
                mat = fitz.Matrix(scale, scale)

                # Render the page with the scaling matrix
                pix = page.get_pixmap(matrix=mat)

                # Convert the pixmap to bytes in PNG format
                image_data = pix.tobytes(output='jpeg')
                pages_content.append(PageContent(page_number=page_num, image_data=image_data))
            else:
                # No images, extract text
                text = page.get_text()
                pages_content.append(PageContent(page_number=page_num, text=text))

        return pages_content
