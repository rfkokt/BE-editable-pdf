import fitz  # PyMuPDF
import io
from typing import BinaryIO

def resize_pdf(file: BinaryIO, scale_factor: float) -> io.BytesIO:
    """
    Mengubah ukuran semua halaman dalam file PDF dengan faktor skala yang diberikan,
    sambil mempertahankan kualitas asli.

    Args:
    file (BinaryIO): File PDF yang akan diubah ukurannya.
    scale_factor (float): Faktor skala untuk mengubah ukuran PDF. 
                          1.0 adalah ukuran asli, 2.0 akan memperbesar dua kali lipat, 0.5 akan memperkecil setengahnya.

    Returns:
    io.BytesIO: Objek BytesIO yang berisi PDF yang telah diubah ukurannya.

    Raises:
    ValueError: Jika scale_factor kurang dari atau sama dengan 0.
    """
    if scale_factor <= 0:
        raise ValueError("scale_factor harus lebih besar dari 0")

    try:
        pdf_document = fitz.open(stream=file.read(), filetype="pdf")
        
        for page in pdf_document:
            # Dapatkan matriks transformasi untuk scaling
            matrix = fitz.Matrix(scale_factor, scale_factor)
            
            # Terapkan transformasi ke semua elemen di halaman
            page.apply_transform(matrix)

        output = io.BytesIO()
        pdf_document.save(output, garbage=4, deflate=True, clean=True)
        pdf_document.close()
        output.seek(0)
        return output
    
    except Exception as e:
        raise RuntimeError(f"Terjadi kesalahan saat mengubah ukuran PDF: {str(e)}")