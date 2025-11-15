import io
import os
from typing import List

import streamlit as st
from pypdf import PdfWriter
import io
import os


def merge_pdfs_with_bookmarks(files):
    """
    Merge uploaded PDF files into a single PDF, adding a top-level
    bookmark (outline item) for each original file, using the filename
    (without extension) as the title.

    Uses pypdf.PdfWriter.append(), which is the modern, supported API.
    """
    writer = PdfWriter()

    # Sort by filename so order is predictable
    files_sorted = sorted(files, key=lambda f: f.name.lower())

    for uploaded_file in files_sorted:
        # Streamlit gives us a file-like object; rewind just in case
        uploaded_file.seek(0)

        base_name = os.path.splitext(uploaded_file.name)[0]

        # Append the entire PDF and create a bookmark at its first page
        # outline_item is the bookmark title
        writer.append(uploaded_file, outline_item=base_name)

    # Write merged PDF to a BytesIO buffer
    output_stream = io.BytesIO()
    writer.write(output_stream)
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
