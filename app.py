import streamlit as st
import requests

st.set_page_config(page_title="DFMEA GenAI", layout="centered")
st.title("🧠 DFMEA Generator (via FastAPI)")

kb_url = st.text_input("📎 Knowledge Bank File URL")
fi_url = st.text_input("📎 Field Reported Issues File URL")
query = st.text_area("📝 Prompt", value="Generate DFMEA entries for recent field failures")

if st.button("🚀 Run Full DFMEA Pipeline"):
    try:
        with st.spinner("Running DFMEA pipeline via FastAPI..."):
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
                st.success("✅ DFMEA completed!")
                # st.markdown(f"[⬇ Download DFMEA Excel File]({result['output_file_url']})", unsafe_allow_html=True)
                download_url = result['output_file_url']
                download_resp = requests.get(download_url)

                st.download_button(
                    label="⬇ Download DFMEA Excel File",
                    data=download_resp.content,
                    file_name="dfmea_output.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error("❌ Pipeline failed.")

    except Exception as e:
        st.error(f"Error: {e}")
