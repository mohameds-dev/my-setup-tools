# Image Resizer

A single-file HTML tool to resize and compress photos and scanned documents to fit common upload size limits (<1MB, <5MB, <10MB, <20MB).

## Usage
Open `index.html` in any browser:
1. Select an image file.
2. Choose target size.
3. Click Resize and download the output.

## Technical Details
- Runs entirely in the browser using the HTML5 Canvas API.
- Zero network requests and zero external dependencies.
- Adjusts JPEG compression quality first, then downscales dimensions if needed to preserve text legibility.
