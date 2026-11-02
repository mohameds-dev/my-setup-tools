# custom_pdf_tools

A pure, modular, and expandable PDF utility toolsuite written in Python and managed with `uv`.

The primary tool is **PDF Rasterization**: it converts each page of a PDF into high-resolution rendered pixels and rebuilds a clean PDF. This ensures all hidden text, OCR text layers, invisible fonts, annotations, form metadata, and vector layers are completely stripped while preserving exact visual appearance, page count, and page dimensions.

---

## Features

- **True Rasterization**: Renders PDF pages to images and rebuilds the PDF. Selectable and hidden text is completely eliminated.
- **Visual & Dimensional Fidelity**: Preserves original page sizes (MediaBox) and aspect ratios across pages (including mixed portrait and landscape).
- **Fast & Memory Efficient**: Powered by Google Chromium's PDFium engine (`pypdfium2`) and zero-loss direct embedding via `img2pdf`.
- **Pure & Reusable**: Can be used directly from the command line or imported as a clean Python library.
- **Configurable**: Control DPI resolution, intermediate formats (`jpeg`, `png`), JPEG quality, and grayscale conversion.
- **Expandable**: Built with a modular subcommand architecture ready for future PDF tools.

---

## Installation & Setup

Ensure [`uv`](https://docs.astral.sh/uv/) is installed on your machine.

Clone or navigate to the project directory:

```bash
cd custom_pdf_tools
uv sync
```

This will automatically create a `.venv` virtual environment and install all dependencies locked in `uv.lock`.

---

## Command Line Usage

You can run the tool in any of the following ways:

### 1. Direct Execution
```bash
# Basic usage: custom-pdf-tools <input_path> <output_path>
uv run custom-pdf-tools document.pdf rasterized.pdf

# Or use the rasterize-pdf alias
uv run rasterize-pdf document.pdf rasterized.pdf

# Or run via Python module
uv run python -m custom_pdf_tools document.pdf rasterized.pdf
```

### 2. Subcommand Form
```bash
uv run custom-pdf-tools rasterize input.pdf output.pdf --dpi 300
```

### CLI Options

| Option | Type | Default | Description |
|---|---|---|---|
| `input` | Path | *Required* | Path to input PDF file |
| `output` | Path | *Required* | Path for the output rasterized PDF |
| `--dpi` | Integer | `300` | Rendering resolution in DPI (e.g. 150, 300, 600) |
| `--format` | `jpeg` \| `png` | `jpeg` | Intermediate image format. Use `png` for lossless output |
| `--quality` | Integer (1-100) | `85` | JPEG quality level (ignored if format is `png`) |
| `--grayscale` | Flag | `False` | Render pages in grayscale |
| `-q`, `--quiet` | Flag | `False` | Suppress console output messages |
| `-h`, `--help` | Flag | | Show help and available options |
| `--version` | Flag | | Show version information |

### Examples

```bash
# High-resolution (300 DPI, default JPEG quality 85)
uv run custom-pdf-tools confidential_doc.pdf clean_doc.pdf

# Lossless PNG rasterization at 400 DPI
uv run custom-pdf-tools document.pdf output.pdf --format png --dpi 400

# Grayscale rasterization at 150 DPI with high JPEG quality
uv run custom-pdf-tools scanned.pdf clean.pdf --grayscale --dpi 150 --quality 95
```

---

## Python API Usage

You can import and use `custom_pdf_tools` directly in other Python projects:

```python
from pathlib import Path
from custom_pdf_tools import rasterize_pdf, RasterizeOptions

# Quick call
output_path = rasterize_pdf("input.pdf", "output.pdf", dpi=300)

# Or with RasterizeOptions
options = RasterizeOptions(
    dpi=300,
    image_format="jpeg",
    quality=90,
    grayscale=False,
)
rasterize_pdf(Path("input.pdf"), Path("output.pdf"), options=options)
```

---

## Running Tests

Run the full test suite and coverage reports:

```bash
uv run pytest --cov=custom_pdf_tools --cov-report=term-missing
```
