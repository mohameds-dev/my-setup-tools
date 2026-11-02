from dataclasses import dataclass
from pathlib import Path
import tempfile
from typing import Literal
import img2pdf
import pypdfium2 as pdfium


@dataclass
class RasterizeOptions:
    dpi: int = 300
    image_format: Literal["jpeg", "jpg", "png"] = "jpeg"
    quality: int = 85
    grayscale: bool = False

    def __post_init__(self) -> None:
        if self.dpi <= 0:
            raise ValueError(f"DPI must be positive, got {self.dpi}")
        normalized_format = self.image_format.lower()
        if normalized_format not in ("jpeg", "jpg", "png"):
            raise ValueError(f"Unsupported image format: {self.image_format}. Use 'jpeg' or 'png'.")
        self.image_format = normalized_format
        if not (1 <= self.quality <= 100):
            raise ValueError(f"Quality must be between 1 and 100, got {self.quality}")


def rasterize_pdf(
    input_path: str | Path,
    output_path: str | Path,
    dpi: int | None = None,
    image_format: str | None = None,
    quality: int | None = None,
    grayscale: bool | None = None,
    options: RasterizeOptions | None = None,
) -> Path:
    """
    Rasterize a PDF: renders each page to a high-resolution raster image and converts
    the images back into a clean, text-free PDF matching original visual dimensions.
    """
    in_path = Path(input_path).resolve()
    if not in_path.is_file():
        raise FileNotFoundError(f"Input PDF file not found: {input_path}")

    out_path = Path(output_path).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Resolve options
    opts = options or RasterizeOptions()
    if dpi is not None:
        opts.dpi = dpi
    if image_format is not None:
        opts.image_format = image_format
    if quality is not None:
        opts.quality = quality
    if grayscale is not None:
        opts.grayscale = grayscale
    opts.__post_init__()

    doc = pdfium.PdfDocument(str(in_path))
    num_pages = len(doc)
    scale = opts.dpi / 72.0
    pil_format = "PNG" if opts.image_format == "png" else "JPEG"
    ext = "png" if opts.image_format == "png" else "jpg"

    with tempfile.TemporaryDirectory(prefix="custom_pdf_rasterize_") as temp_dir:
        temp_dir_path = Path(temp_dir)
        image_paths: list[str] = []

        for i in range(num_pages):
            page = doc[i]
            bitmap = page.render(
                scale=scale,
                grayscale=opts.grayscale,
                draw_annots=True,
                may_draw_forms=True,
            )
            pil_image = bitmap.to_pil()
            page_img_path = temp_dir_path / f"page_{i:05d}.{ext}"

            save_kwargs = {"dpi": (opts.dpi, opts.dpi)}
            if pil_format == "JPEG":
                save_kwargs["quality"] = opts.quality
                save_kwargs["optimize"] = True

            pil_image.save(page_img_path, format=pil_format, **save_kwargs)
            image_paths.append(str(page_img_path))

        doc.close()

        with open(out_path, "wb") as f_out:
            img2pdf.convert(image_paths, outputstream=f_out)

    return out_path
