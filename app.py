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
st.write(
    """
    Welcome to the AlphaFold Server CIF to PDB Converter!
    This app allows you to upload ZIP files, downloaded from the AlphaFold server (containing .cif files),
    extracts the contents, converts the .cif files to .pdb format, and re-zips everything for download.
    """
)
# File uploader
uploaded_files = st.file_uploader("Upload ZIP files containing .cif files", type="zip", accept_multiple_files=True)
output_folder_name = st.text_input("Output folder name", "converted_files.zip")

if uploaded_files:
    progress_text = st.empty()
    progress_bar = st.progress(0)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)

        # Process each uploaded ZIP file
        total_files = len(uploaded_files)
        for i, uploaded_file in enumerate(uploaded_files):
            progress_text.text(f"Processing file {i + 1} of {total_files}")
            zip_name = Path(uploaded_file.name).stem
            zip_extract_path = temp_dir_path / zip_name
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

        # Show spinning wheel
        with st.spinner('Creating final ZIP file...'):
            time.sleep(1)  # Simulate some processing time

            # Create a final ZIP file containing all converted folders
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_zip:
                final_output_zip = temp_zip.name
                with zipfile.ZipFile(final_output_zip, 'w') as zipf:
                    for folder in temp_dir_path.iterdir():
                        for file in folder.iterdir():
                            zipf.write(file, arcname=f"{folder.name}/{file.name}")

        # Display download link for the ZIP file
        with open(final_output_zip, "rb") as f:
            st.download_button(
                label="Download",
                data=f,
                file_name=output_folder_name,
                mime="application/zip",
                type='primary',
                use_container_width=True
            )

        # Clean up temporary files
        try:
            os.remove(final_output_zip)
        except PermissionError:
            st.error(f"Permission denied while trying to remove {final_output_zip}")
