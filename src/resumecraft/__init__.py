from importlib.metadata import version

from resumecraft.craft import ResumeCraft

__version__ = version("resumecraft")
__all__ = ["ResumeCraft", "__version__"]
