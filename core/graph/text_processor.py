"""
Servicio de procesamiento de texto
"""

from typing import List
from ..utils.file_parser import FileParser, split_text_into_chunks


class TextProcessor:
    """Procesador de texto"""

    @staticmethod
    def extract_from_files(file_paths: List[str]) -> str:
        """Extraer texto de múltiples archivos"""
        return FileParser.extract_from_multiple(file_paths)

    @staticmethod
    def split_text(
        text: str,
        chunk_size: int = 500,
        overlap: int = 50
    ) -> List[str]:
        """Dividir texto en chunks."""
        return split_text_into_chunks(text, chunk_size, overlap)

    @staticmethod
    def preprocess_text(text: str) -> str:
        """Normalizar saltos de línea y espacios redundantes."""
        import re

        text = text.replace('\r\n', '\n').replace('\r', '\n')
        text = re.sub(r'\n{3,}', '\n\n', text)
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)
        return text.strip()

    @staticmethod
    def get_text_stats(text: str) -> dict:
        """Obtener estadísticas del texto."""
        return {
            "total_chars": len(text),
            "total_lines": text.count('\n') + 1,
            "total_words": len(text.split()),
        }

