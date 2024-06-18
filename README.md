## AlphaFold Server CIF to PDB Converter

Welcome to the AlphaFold Server CIF to PDB Converter! This simple Streamlit app allows you to upload ZIP files containing `.cif` files from the AlphaFold server, converts them to `.pdb` format, and provides a downloadable ZIP file with the converted files.

#### Check it out on the streamlit cloud: [https://af-pdb.streamlit.app](https://af-pdb.streamlit.app/)

### Features
- **Multiple ZIP File Upload**: Upload multiple ZIP files in one go.
- **Automatic Conversion**: Converts `.cif` files to `.pdb` format seamlessly.
- **Organized Output**: Keeps the original folder structure within the final ZIP file.

### How to Use
1. **Upload ZIP Files**: Click on the "Upload ZIP files containing .cif files" button to select and upload one or more ZIP files.
2. **Specify Output Name**: Enter the desired name for the output ZIP file in the "Output folder name" field.
3. **Process Files**: The app will extract the contents of the uploaded ZIP files, convert `.cif` files to `.pdb`, and re-zip everything.
4. **Download**: Once processing is complete, click the "Download" button to download the final ZIP file containing all converted files.

### Requirements
- Streamlit
- BioPython

### Installation
To run the app locally, follow these steps:
1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/alphafold-converter.git
    ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```