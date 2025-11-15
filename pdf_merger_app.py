import io
import os
from typing import List

import streamlit as st
from pypdf import PdfMerger
import io
import os


def merge_pdfs_with_bookmarks(files):
    """
    Merge uploaded PDF files into a single PDF, adding a top-level
    bookmark for each original file, using the filename (without extension)
    as the bookmark title.

    Uses PdfMerger to preserve fonts/layout as-is.
    """
    merger = PdfMerger()

    # Sort by filename so order is predictable
    files_sorted = sorted(files, key=lambda f: f.name.lower())

    for uploaded_file in files_sorted:
        # Read the uploaded file into memory (Streamlit gives a file-like object)
        uploaded_file.seek(0)
        pdf_bytes = uploaded_file.read()
        pdf_stream = io.BytesIO(pdf_bytes)

        base_name = os.path.splitext(uploaded_file.name)[0]

        # Append with a bookmark. This keeps the original pages untouched.
        merger.append(pdf_stream, bookmark=base_name)

    # Write merged PDF to a BytesIO buffer
    output_stream = io.BytesIO()
    merger.write(output_stream)
    merger.close()
    output_stream.seek(0)
    return output_stream

def main():
    st.set_page_config(page_title="PDF Combiner with Bookmarks", layout="centered")

    st.title("📚 PDF Combiner with Bookmarks")
    st.write(
        "Upload multiple PDF files and I’ll merge them into a single PDF "
        "with bookmarks for each original file."
    )

    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    st.info("Tip: Filenames are used as bookmark titles. Order is sorted by filename.")

    if uploaded_files:
        st.write("### Files to merge (sorted by name):")
        for f in sorted(uploaded_files, key=lambda x: x.name.lower()):
            st.write(f"- {f.name}")

        merged_filename = st.text_input(
            "Output filename (no extension):",
            value="merged_document"
        )

        if st.button("🔗 Merge PDFs"):
            with st.spinner("Merging PDFs..."):
                merged_pdf = merge_pdfs_with_bookmarks(uploaded_files)

            st.success("Done! Download your merged PDF below:")
            st.download_button(
                label="⬇️ Download merged PDF",
                data=merged_pdf,
                file_name=f"{merged_filename}.pdf",
                mime="application/pdf",
            )


if __name__ == "__main__":
    main()
