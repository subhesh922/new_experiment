import streamlit as st
import requests

st.set_page_config(page_title="DFMEA GenAI", layout="centered")
st.title("🧠 DFMEA Generator")

kb_url = st.text_input("📎 Knowledge Bank File URL")
fi_url = st.text_input("📎 Field Reported Issues File URL")
query = st.text_area("📝 Prompt", value="Generate DFMEA entries for recent field failures")

if st.button("🔧 Generate DFMEA Report"):
    try:
        with st.spinner("Running full DFMEA pipeline via FastAPI..."):
            resp = requests.post(
                "http://localhost:8000/run_dfmea",
                json={
                    "kb_url": kb_url,
                    "fi_url": fi_url,
                    "query": query
                }
            )
            resp.raise_for_status()
            result = resp.json()

            if result["status"] == "success":
                st.success("✅ DFMEA report successfully generated!")

                # Fetch the actual Excel file
                download_url = result["output_file_url"]
                download_resp = requests.get(download_url)

                if download_resp.status_code == 200:
                    st.download_button(
                        label="⬇ Click here to download the DFMEA Excel file",
                        data=download_resp.content,
                        file_name="dfmea_output.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.warning("⚠️ Unable to fetch Excel file. It may have been deleted.")
            else:
                st.error("❌ DFMEA pipeline failed. Please try again.")

    except Exception as e:
        st.error(f"❌ Error: {e}")
