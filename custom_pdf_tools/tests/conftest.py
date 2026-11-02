import pytest
from pathlib import Path
import pikepdf


@pytest.fixture
def sample_pdf_with_text(tmp_path: Path) -> Path:
    """Creates a sample PDF containing visible and invisible/hidden text."""
    pdf = pikepdf.new()
    page = pdf.add_blank_page(page_size=(300, 400))
    font = pdf.make_indirect(pikepdf.Dictionary(
        Type=pikepdf.Name.Font,
        Subtype=pikepdf.Name.Type1,
        BaseFont=pikepdf.Name.Helvetica
    ))
    page.Resources = pikepdf.Dictionary(
        Font=pikepdf.Dictionary(F1=font)
    )
    # Render mode 0 = Fill text (visible), Render mode 3 = Neither fill nor stroke (invisible/hidden text)
    content = (
        b"BT /F1 20 Tf 50 300 Td (Visible Title Text) Tj ET\n"
        b"BT /F1 12 Tf 3 Tr 50 200 Td (Classified Hidden Password) Tj ET"
    )
    page.Contents = pdf.make_stream(content)
    pdf_path = tmp_path / "sample_text.pdf"
    pdf.save(str(pdf_path))
    return pdf_path


@pytest.fixture
def multi_page_mixed_pdf(tmp_path: Path) -> Path:
    """Creates a multi-page PDF with differing page sizes."""
    pdf = pikepdf.new()
    font = pdf.make_indirect(pikepdf.Dictionary(
        Type=pikepdf.Name.Font,
        Subtype=pikepdf.Name.Type1,
        BaseFont=pikepdf.Name.Helvetica
    ))

    # Page 1: Portrait 300x400
    p1 = pdf.add_blank_page(page_size=(300, 400))
    p1.Resources = pikepdf.Dictionary(Font=pikepdf.Dictionary(F1=font))
    p1.Contents = pdf.make_stream(b"BT /F1 16 Tf 30 350 Td (Page 1 Text) Tj ET")

    # Page 2: Landscape 500x300
    p2 = pdf.add_blank_page(page_size=(500, 300))
    p2.Resources = pikepdf.Dictionary(Font=pikepdf.Dictionary(F1=font))
    p2.Contents = pdf.make_stream(b"BT /F1 16 Tf 50 150 Td (Page 2 Text) Tj ET")

    pdf_path = tmp_path / "multi_page.pdf"
    pdf.save(str(pdf_path))
    return pdf_path
