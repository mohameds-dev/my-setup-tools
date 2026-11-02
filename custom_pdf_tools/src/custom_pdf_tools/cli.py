import argparse
import sys
from pathlib import Path
from custom_pdf_tools.rasterize import rasterize_pdf, RasterizeOptions

__version__ = "0.1.0"

SUBCOMMANDS = {"rasterize"}


def _add_raster_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "input",
        help="Path to the input PDF file.",
    )
    parser.add_argument(
        "output",
        help="Path for the output rasterized PDF file.",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Rendering resolution in DPI (default: 300).",
    )
    parser.add_argument(
        "--format",
        choices=["jpeg", "jpg", "png"],
        default="jpeg",
        help="Intermediate image format (default: jpeg). Use 'png' for lossless output.",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=85,
        help="JPEG compression quality between 1 and 100 (default: 85).",
    )
    parser.add_argument(
        "--grayscale",
        action="store_true",
        help="Convert pages to grayscale.",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress output messages.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="custom-pdf-tools",
        description="Suite of pure, modular PDF tools. Convert PDFs to pixel-rasterized PDFs removing hidden text.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(dest="subcommand", title="subcommands")
    raster_sub = subparsers.add_parser(
        "rasterize",
        help="Rasterize a PDF into images and back to PDF, stripping selectable and hidden text.",
    )
    _add_raster_arguments(raster_sub)

    return parser


def normalize_args(args: list[str]) -> list[str]:
    """
    If no known subcommand or top-level flag is the first argument,
    default to the 'rasterize' subcommand for ergonomic usage:
    `custom-pdf-tools input.pdf output.pdf` -> `custom-pdf-tools rasterize input.pdf output.pdf`
    """
    if not args:
        return args

    first = args[0]
    if first in SUBCOMMANDS or first in ("-h", "--help", "-v", "--version"):
        return args

    # Check if first starts with '-' (like --dpi) or is an input path
    # If it's not a top-level option, treat command as implicit 'rasterize'
    return ["rasterize"] + args


def main(args: list[str] | None = None) -> int:
    if args is None:
        args = sys.argv[1:]

    args = normalize_args(args)
    parser = build_parser()

    if not args:
        parser.print_help()
        return 1

    try:
        parsed = parser.parse_args(args)
    except SystemExit as exc:
        return exc.code if isinstance(exc.code, int) else 1

    if parsed.subcommand == "rasterize":
        input_path = Path(parsed.input)
        output_path = Path(parsed.output)

        try:
            options = RasterizeOptions(
                dpi=parsed.dpi,
                image_format=parsed.format,
                quality=parsed.quality,
                grayscale=parsed.grayscale,
            )
            if not parsed.quiet:
                print(f"Rasterizing '{input_path}' -> '{output_path}' ({options.dpi} DPI, {options.image_format})...")

            result = rasterize_pdf(input_path, output_path, options=options)

            if not parsed.quiet:
                print(f"Successfully created: {result}")
            return 0
        except Exception as exc:
            sys.stderr.write(f"Error: {exc}\n")
            return 1

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
