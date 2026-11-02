from pathlib import Path
import pytest
import pypdfium2 as pdfium
from custom_pdf_tools.rasterize import rasterize_pdf, RasterizeOptions


def extract_all_text(pdf_path: Path) -> str:
    doc = pdfium.PdfDocument(str(pdf_path))
    texts = []
    for page in doc:
        tp = page.get_textpage()
        texts.append(tp.get_text_range())
    return "".join(texts)


def get_page_sizes(pdf_path: Path) -> list[tuple[float, float]]:
    doc = pdfium.PdfDocument(str(pdf_path))
    return [page.get_size() for page in doc]


def test_rasterize_removes_selectable_and_hidden_text(sample_pdf_with_text: Path, tmp_path: Path):
    # Verify original has text (both visible and hidden)
    orig_text = extract_all_text(sample_pdf_with_text)
    assert "Visible Title Text" in orig_text
    assert "Classified Hidden Password" in orig_text

    output_pdf = tmp_path / "rasterized.pdf"
    result = rasterize_pdf(sample_pdf_with_text, output_pdf, dpi=150)

    assert result == output_pdf
    assert output_pdf.exists()
    assert output_pdf.stat().st_size > 0

    # Verify rasterized PDF has no selectable text at all
    rasterized_text = extract_all_text(output_pdf)
    assert rasterized_text.strip() == ""
    assert "Visible Title Text" not in rasterized_text
    assert "Classified Hidden Password" not in rasterized_text


def test_rasterize_preserves_page_count_and_dimensions(multi_page_mixed_pdf: Path, tmp_path: Path):
    orig_sizes = get_page_sizes(multi_page_mixed_pdf)
    assert len(orig_sizes) == 2
    assert orig_sizes[0] == (300.0, 400.0)
    assert orig_sizes[1] == (500.0, 300.0)

    output_pdf = tmp_path / "mixed_rasterized.pdf"
    rasterize_pdf(multi_page_mixed_pdf, output_pdf, dpi=200)

    new_sizes = get_page_sizes(output_pdf)
    assert len(new_sizes) == 2
    # Allow small rounding tolerance within 1 point due to pixel to point conversion
    assert abs(new_sizes[0][0] - 300.0) <= 1.0
    assert abs(new_sizes[0][1] - 400.0) <= 1.0
    assert abs(new_sizes[1][0] - 500.0) <= 1.0
    assert abs(new_sizes[1][1] - 300.0) <= 1.0


def test_rasterize_options_png_and_grayscale(sample_pdf_with_text: Path, tmp_path: Path):
    output_pdf = tmp_path / "rasterized_png_gray.pdf"
    options = RasterizeOptions(dpi=100, image_format="png", grayscale=True)
    rasterize_pdf(sample_pdf_with_text, output_pdf, options=options)

    assert output_pdf.exists()
    assert extract_all_text(output_pdf).strip() == ""


def test_rasterize_creates_parent_directory(sample_pdf_with_text: Path, tmp_path: Path):
    nested_output = tmp_path / "deep" / "nested" / "dir" / "out.pdf"
    rasterize_pdf(sample_pdf_with_text, nested_output)
    assert nested_output.exists()


def test_rasterize_overwrites_existing_output(sample_pdf_with_text: Path, tmp_path: Path):
    out_pdf = tmp_path / "out_overwrite.pdf"
    out_pdf.write_text("dummy")
    assert out_pdf.read_text() == "dummy"

    rasterize_pdf(sample_pdf_with_text, out_pdf)
    assert out_pdf.stat().st_size > 0
    # Must now be a valid PDF
    doc = pdfium.PdfDocument(str(out_pdf))
    assert len(doc) == 1


def test_rasterize_raises_on_nonexistent_file(tmp_path: Path):
    non_existent = tmp_path / "does_not_exist.pdf"
    output = tmp_path / "out.pdf"
    with pytest.raises(FileNotFoundError):
        rasterize_pdf(non_existent, output)


def test_rasterize_raises_on_invalid_options(sample_pdf_with_text: Path, tmp_path: Path):
    output = tmp_path / "out.pdf"
    with pytest.raises(ValueError, match="DPI must be positive"):
        rasterize_pdf(sample_pdf_with_text, output, dpi=0)

    with pytest.raises(ValueError, match="Unsupported image format"):
        rasterize_pdf(sample_pdf_with_text, output, image_format="bmp")

    with pytest.raises(ValueError, match="Quality must be between 1 and 100"):
        rasterize_pdf(sample_pdf_with_text, output, quality=150)
