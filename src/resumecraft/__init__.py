from importlib.metadata import version

from resumecraft.builder import DocxBuilder
from resumecraft.models import Resume

__version__ = version("resumecraft")
__all__ = ["Resume", "DocxBuilder", "__version__"]
