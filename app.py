import uuid

import streamlit as st
import zipfile
import os
from pathlib import Path
import tempfile
from Bio import PDB
import time


# Function to convert .cif to .pdb
def convert_cif_to_pdb(cif_file, pdb_file):
    parser = PDB.MMCIFParser()
    structure = parser.get_structure('structure', cif_file)
    io = PDB.PDBIO()
    io.set_structure(structure)
    io.save(pdb_file)


# Set page configuration for better indexing
st.set_page_config(
    page_title="AlphaFold Server CIF to PDB Converter",
    page_icon=":sparkles:",
    layout="centered",
    initial_sidebar_state="auto",
)

# Streamlit app title and description
st.title("AlphaFold Server CIF to PDB Converter")
st.markdown(
    """
    Welcome to the **AlphaFold Server CIF to PDB Converter!**
    This app allows you to upload one or more ZIP files, downloaded from the [AlphaFold server](https://alphafoldserver.com/),
    extracts the contents, converts the **.cif** files to **.pdb** format, and then re-zips everything for download.
    """, unsafe_allow_html=True
)

if 'uploaded_files_key' not in st.session_state:
    st.session_state['uploaded_files_key'] = str(uuid.uuid4())

# File uploader
uploaded_files = st.file_uploader("Upload Alpha Fold Server ZIPs",
                                  type="zip",
                                  accept_multiple_files=True,
                                  key=st.session_state['uploaded_files_key'])
output_folder_name = st.text_input("Output folder name", "converted_files.zip")

btn_empty = st.empty()

if not uploaded_files:
    st.warning("Please upload one or more ZIP files")


if btn_empty.button("Convert", use_container_width=True, disabled=not uploaded_files):
    progress_text = st.empty()

    progress_bar_frame = st.empty()
    progress_bar = progress_bar_frame.progress(0)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)

        extract_path = temp_dir_path / "extracted_files"

        # make the dir
        extract_path.mkdir(exist_ok=True)

        # Process each uploaded ZIP file
        total_files = len(uploaded_files)
        for i, uploaded_file in enumerate(uploaded_files):
            progress_text.text(f"Processing file {i + 1} of {total_files}")
            zip_name = Path(uploaded_file.name).stem
            zip_extract_path = extract_path / zip_name
            zip_extract_path.mkdir(exist_ok=True)

            with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                zip_ref.extractall(zip_extract_path)

            # Convert .cif files to .pdb
            cif_files = list(zip_extract_path.glob("*.cif"))
            if cif_files:
                for cif_file in cif_files:
                    pdb_file = cif_file.with_suffix('.pdb')
                    convert_cif_to_pdb(str(cif_file), str(pdb_file))

            # Update progress bar
            progress_bar.progress((i + 1) / total_files)
            time.sleep(0.5)

        progress_bar_frame.empty()
        progress_text.empty()

        # Show spinning wheel
        with st.spinner('Creating final ZIP file...'):

            # Create a final ZIP file containing all converted folders
            final_output_zip_path = temp_dir_path / "converted_files.zip"
            with zipfile.ZipFile(final_output_zip_path, 'w') as zipf:
                for folder in extract_path.iterdir():
                    for file in folder.iterdir():
                        zipf.write(file, arcname=f"{folder.name}/{file.name}")

        # Display download link for the ZIP file
        with open(final_output_zip_path, "rb") as f:
            if btn_empty.download_button(
                    label="Download",
                    data=f,
                    file_name=output_folder_name,
                    mime="application/zip",
                    type='primary',
                    use_container_width=True
            ):
                st.session_state['uploaded_files_key'] = str(uuid.uuid4())
                st.rerun()
