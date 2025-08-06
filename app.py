import streamlit as st
import os
import requests
from server.pipeline.end_to_end_pipeline import DFMEAEndToEndPipeline

st.set_page_config(page_title="DFMEA Generator", layout="centered")

st.title("📊 DFMEA GenAI Platform")

# --- Input Section ---
st.header("📁 Provide input files")

kb_url = st.text_input("Knowledge Bank File URL (CSV/XLSX)")
fi_url = st.text_input("Field Reported Issues File URL (CSV/XLSX)")
query = st.text_area("DFMEA Prompt", value="Generate DFMEA entries for recent field failures")

# --- Helper to download and save file ---
def download_file(url: str, save_path: str):
    r = requests.get(url)
    r.raise_for_status()
    with open(save_path, "wb") as f:
        f.write(r.content)

# --- Run button ---
if st.button("🚀 Run DFMEA Pipeline"):

    try:
        # Ensure sample_files folder exists
        os.makedirs("server/sample_files", exist_ok=True)

        # Download input files
        kb_path = "server/sample_files/kb_input.xlsx" if "xlsx" in kb_url else "server/sample_files/kb_input.csv"
        fi_path = "server/sample_files/fi_input.xlsx" if "xlsx" in fi_url else "server/sample_files/fi_input.csv"
        download_file(kb_url, kb_path)
        download_file(fi_url, fi_path)

        st.info("📥 Files downloaded successfully. Running pipeline...")

        # Run pipeline
        pipeline = DFMEAEndToEndPipeline(kb_path=kb_path, fi_path=fi_path, query=query, top_k=100)
        output_path = pipeline.run()

        # Display download link
        st.success("✅ DFMEA Pipeline complete!")
        with open(output_path, "rb") as f:
            st.download_button("⬇ Download DFMEA Excel", f, file_name="dfmea_output.xlsx")

    except Exception as e:
        st.error(f"❌ Error: {e}")
