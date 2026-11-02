#!/usr/bin/env bash
set -euo pipefail

# Determine script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Resolve input directory (pdf_files)
if [[ -d "${SCRIPT_DIR}/pdf_files" ]]; then
    INPUT_DIR="${SCRIPT_DIR}/pdf_files"
elif [[ -d "pdf_files" ]]; then
    INPUT_DIR="$(cd "pdf_files" && pwd)"
else
    echo "Error: Directory 'pdf_files' not found in '${SCRIPT_DIR}' or current working directory." >&2
    exit 1
fi

OUTPUT_DIR="${INPUT_DIR}/rasterized"
mkdir -p "${OUTPUT_DIR}"

# Collect all .pdf files directly under INPUT_DIR
shopt -s nullglob
pdf_files=("${INPUT_DIR}"/*.pdf)
shopt -u nullglob

if [[ ${#pdf_files[@]} -eq 0 ]]; then
    echo "No .pdf files found under '${INPUT_DIR}'."
    exit 0
fi

echo "Found ${#pdf_files[@]} PDF file(s) in '${INPUT_DIR}'."
echo "Output directory: '${OUTPUT_DIR}'"
echo "----------------------------------------"

success_count=0
fail_count=0

for file in "${pdf_files[@]}"; do
    filename="$(basename "${file}")"
    out_file="${OUTPUT_DIR}/${filename}"

    echo "Processing: ${filename} ..."
    if (cd "${SCRIPT_DIR}" && uv run custom-pdf-tools "${file}" "${out_file}" "$@"); then
        success_count=$((success_count + 1))
    else
        echo "Failed to rasterize: ${filename}" >&2
        fail_count=$((fail_count + 1))
    fi
    echo "----------------------------------------"
done

echo "Rasterization complete."
echo "Successfully rasterized: ${success_count}"
if [[ ${fail_count} -gt 0 ]]; then
    echo "Failed: ${fail_count}" >&2
    exit 1
fi

exit 0
