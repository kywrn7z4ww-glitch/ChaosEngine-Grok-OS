"""
mirroring package — GrokOS Mirror Logic Module

This package contains the batch mirroring implementation and Download Skill glue.

Public API:
    from mirroring import run_mirror_logic, download
    from mirroring.mirror_logic import run_mirror_logic
    from mirroring.download_skill import download, download_file_list
"""

from .download_skill import download, download_file_list
from .mirror_logic import run_mirror_logic

__version__ = "0.2"
__all__ = ["run_mirror_logic", "download", "download_file_list"]
