import subprocess
import sys
from pathlib import Path
import pypdfium2 as pdfium
from custom_pdf_tools.cli import main


def test_cli_basic_rasterize(sample_pdf_with_text: Path, tmp_path: Path):
    output_pdf = tmp_path / "cli_out.pdf"
    exit_code = main([str(sample_pdf_with_text), str(output_pdf)])
    assert exit_code == 0
    assert output_pdf.exists()

    doc = pdfium.PdfDocument(str(output_pdf))
    assert len(doc) == 1
    assert doc[0].get_textpage().get_text_range().strip() == ""


def test_cli_subcommand_rasterize(sample_pdf_with_text: Path, tmp_path: Path):
    output_pdf = tmp_path / "cli_sub_out.pdf"
    exit_code = main(["rasterize", str(sample_pdf_with_text), str(output_pdf), "--dpi", "150"])
    assert exit_code == 0
    assert output_pdf.exists()


def test_cli_with_all_options(sample_pdf_with_text: Path, tmp_path: Path):
    output_pdf = tmp_path / "cli_opts_out.pdf"
    exit_code = main([
        str(sample_pdf_with_text),
        str(output_pdf),
        "--dpi", "120",
        "--format", "png",
        "--grayscale",
        "--quality", "95",
        "--quiet",
    ])
    assert exit_code == 0
    assert output_pdf.exists()


def test_cli_missing_input_file(tmp_path: Path):
    exit_code = main([str(tmp_path / "nonexistent.pdf"), str(tmp_path / "out.pdf")])
    assert exit_code != 0


def test_cli_invalid_dpi(sample_pdf_with_text: Path, tmp_path: Path):
    exit_code = main([str(sample_pdf_with_text), str(tmp_path / "out.pdf"), "--dpi", "-5"])
    assert exit_code != 0


def test_cli_no_args():
    exit_code = main([])
    assert exit_code != 0


def test_cli_subprocess_execution(sample_pdf_with_text: Path, tmp_path: Path):
    output_pdf = tmp_path / "cli_proc_out.pdf"
    res = subprocess.run(
        [sys.executable, "-m", "custom_pdf_tools", str(sample_pdf_with_text), str(output_pdf)],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    assert output_pdf.exists()
    assert "Successfully created:" in res.stdout
