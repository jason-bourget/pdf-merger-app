import io
import os
from typing import List

import streamlit as st
from PyPDF2 import PdfReader, PdfWriter


def merge_pdfs_with_bookmarks(files: List) -> io.BytesIO:
    """
    Merge uploaded PDF files into a single PDF, adding a top-level
    bookmark for each original file, using the filename (without extension)
    as the bookmark title.
    """
    writer = PdfWriter()
    current_page = 0

    # Sort by filename so order is predictable
    files_sorted = sorted(files, key=lambda f: f.name.lower())

    for uploaded_file in files_sorted:
        reader = PdfReader(uploaded_file)
        num_pages = len(reader.pages)

        # Add pages
        for page in reader.pages:
            writer.add_page(page)

        # Use the file name (no extension) as the bookmark title
        base_name = os.path.splitext(uploaded_file.name)[0]

        # Add bookmark at the first page of this document
        try:
            # Newer PyPDF2
            writer.add_outline_item(
                title=base_name,
                page_number=current_page
            )
        except AttributeError:
            # Older PyPDF2 fallback
            writer.addBookmark(base_name, current_page)

        current_page += num_pages

    # Write to in-memory buffer
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
