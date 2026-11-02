# Offline Document Image Resizer

A lightweight, completely independent, single-file HTML tool to resize and compress photos/scans of sensitive documents under upload size limits (`<1MB`, `<5MB`, `<10MB`, `<20MB`).

## 🛡️ Privacy & Security
- **100% Offline**: Zero external network requests, zero CDNs, zero analytics, zero cookies.
- **Client-Side Only**: All image processing runs directly inside your local browser via the HTML5 `<canvas>` API. Your images never leave your machine.
- **Fully Verifiable**: All code (HTML, CSS, and JavaScript) is self-contained in a single readable `index.html` file that anyone can inspect.

## 🚀 How to Use
1. Open [`index.html`](file:///home/the_mhmd/projects/linux-env-setup/image_resizer/index.html) in any modern browser (Chrome, Firefox, Safari, Edge, Brave, etc.).
2. Click **"Choose Image"** to pick your scanned document or photo.
3. Select your target maximum size limit (`<1MB`, `<5MB`, `<10MB`, or `<20MB`).
4. Click **"Resize Image"**.
5. Preview the result and click **"Download Resized Image"**.

## 📄 How It Preserves Quality
- Scanned text documents need high sharpness and contrast to remain readable.
- If the original image is already within the target limit, no compression is applied.
- If resizing is required, the tool tests high-to-moderate JPEG qualities first. If needed, it gently downscales resolution in small steps while maintaining high compression quality so text remains crisp and legible.
