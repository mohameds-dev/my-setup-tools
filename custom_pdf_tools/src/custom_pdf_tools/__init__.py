"""
custom_pdf_tools: A pure, modular PDF utility suite.
"""

from custom_pdf_tools.rasterize import rasterize_pdf, RasterizeOptions
from custom_pdf_tools.cli import main

__all__ = ["rasterize_pdf", "RasterizeOptions", "main"]
