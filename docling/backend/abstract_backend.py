from abc import ABC, abstractmethod
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterable, Optional, Union

from docling_core.types.experimental.base import BoundingBox, Size
from PIL import Image

if TYPE_CHECKING:
    from docling.datamodel.base_models import Cell


class AbstractDocumentBackend(ABC):
    @abstractmethod
    def __init__(self, path_or_stream: Union[BytesIO, Path], document_hash: str):
        self.path_or_stream = path_or_stream
        self.document_hash = document_hash

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @abstractmethod
    def unload(self):
        if isinstance(self.path_or_stream, BytesIO):
            self.path_or_stream.close()

        self.path_or_stream = None


class PdfPageBackend(ABC):

    @abstractmethod
    def get_text_in_rect(self, bbox: "BoundingBox") -> str:
        pass

    @abstractmethod
    def get_text_cells(self) -> Iterable["Cell"]:
        pass

    @abstractmethod
    def get_bitmap_rects(self, float: int = 1) -> Iterable["BoundingBox"]:
        pass

    @abstractmethod
    def get_page_image(
        self, scale: float = 1, cropbox: Optional["BoundingBox"] = None
    ) -> Image.Image:
        pass

    @abstractmethod
    def get_size(self) -> "Size":
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @abstractmethod
    def unload(self):
        pass


class PdfDocumentBackend(AbstractDocumentBackend):
    @abstractmethod
    def load_page(self, page_no: int) -> PdfPageBackend:
        pass

    @abstractmethod
    def page_count(self) -> int:
        pass
