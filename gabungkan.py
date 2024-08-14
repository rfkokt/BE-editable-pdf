import PyPDF2
import io
from typing import List
from werkzeug.datastructures import FileStorage

def gabungkan_pdf(file_list: List[FileStorage]) -> io.BytesIO:
    """
    Menggabungkan beberapa file PDF menjadi satu.

    Args:
    file_list (List[FileStorage]): Daftar file PDF yang akan digabungkan.

    Returns:
    io.BytesIO: Objek BytesIO yang berisi PDF yang telah digabungkan.

    Raises:
    ValueError: Jika tidak ada file PDF yang diberikan.
    """
    if not file_list:
        raise ValueError("Tidak ada file PDF yang diberikan")

    pdf_writer = PyPDF2.PdfWriter()

    for file in file_list:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

    output = io.BytesIO()
    pdf_writer.write(output)
    output.seek(0)
    return output