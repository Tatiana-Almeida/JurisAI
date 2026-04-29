from io import BytesIO


class LocalOCREngineUnavailable(Exception):
    """Raised when the optional local OCR engine cannot be used safely."""


class PDFRasterizationUnavailable(Exception):
    """Raised when scanned PDFs cannot be rasterized locally."""


class ScannedPDFOCRUnavailable(Exception):
    """Raised when scanned PDF OCR cannot complete safely."""


class BaseLocalOCREngine:
    provider = 'local'
    model = 'local'

    def is_available(self):
        raise NotImplementedError

    def extract_text_from_image(self, file_bytes):
        raise NotImplementedError

    def extract_text_from_scanned_pdf(self, file_bytes):
        raise ScannedPDFOCRUnavailable('scanned_pdf_local_ocr_not_implemented')


class TesseractOCREngine(BaseLocalOCREngine):
    provider = 'tesseract'
    model = 'tesseract-default'

    def _load_dependencies(self):
        try:
            from PIL import Image
        except ImportError as exc:
            raise LocalOCREngineUnavailable('pillow_not_available') from exc

        try:
            import pytesseract
        except ImportError as exc:
            raise LocalOCREngineUnavailable('pytesseract_not_available') from exc

        return Image, pytesseract

    def is_available(self):
        _, pytesseract = self._load_dependencies()
        try:
            pytesseract.get_tesseract_version()
        except Exception as exc:
            raise LocalOCREngineUnavailable('tesseract_binary_not_available') from exc
        return True

    def extract_text_from_image(self, file_bytes):
        Image, pytesseract = self._load_dependencies()
        self.is_available()

        try:
            with Image.open(BytesIO(file_bytes)) as image:
                return pytesseract.image_to_string(image).strip()
        except LocalOCREngineUnavailable:
            raise
        except Exception as exc:
            raise LocalOCREngineUnavailable('local_image_ocr_failed') from exc

    def extract_text_from_scanned_pdf(self, file_bytes, max_pages=None):
        self.is_available()

        try:
            from pdf2image import convert_from_bytes
        except ImportError as exc:
            raise PDFRasterizationUnavailable('pdf2image_not_available') from exc

        page_limit = max_pages or 10
        try:
            images = convert_from_bytes(file_bytes, first_page=1, last_page=page_limit)
        except Exception as exc:
            raise PDFRasterizationUnavailable('poppler_not_available') from exc

        if not images:
            raise ScannedPDFOCRUnavailable('scanned_pdf_local_ocr_no_pages')

        extracted_pages = []
        for image in images:
            buffer = BytesIO()
            image.save(buffer, format='PNG')
            page_text = self.extract_text_from_image(buffer.getvalue())
            page_text = page_text.strip()
            if page_text:
                extracted_pages.append(page_text)

        extracted_text = '\n\n'.join(extracted_pages).strip()
        if not extracted_text:
            raise ScannedPDFOCRUnavailable('scanned_pdf_local_ocr_no_text')

        return extracted_text


def get_local_ocr_engine(settings):
    provider = getattr(settings, 'preferred_ocr_provider', 'local') or 'local'

    if provider in {'local', 'tesseract'}:
        return TesseractOCREngine()

    raise LocalOCREngineUnavailable('local_ocr_provider_not_supported')
