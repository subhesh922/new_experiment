from fastapi.staticfiles import StaticFiles
from fastapi import Request
from pydantic import BaseModel
import requests

# Mount output folder
app.mount("/files", StaticFiles(directory="server/output"), name="files")

# Request model
class DFMEARequest(BaseModel):
    kb_url: str
    fi_url: str
    query: str = "Generate DFMEA entries for recent field failures"

@app.post("/run_dfmea")
def run_dfmea(req: DFMEARequest):
    kb_path = "server/sample_files/kb_input.xlsx" if "xlsx" in req.kb_url else "server/sample_files/kb_input.csv"
    fi_path = "server/sample_files/fi_input.xlsx" if "xlsx" in req.fi_url else "server/sample_files/fi_input.csv"

    os.makedirs("server/sample_files", exist_ok=True)
import shutil

def download(url, path):
    if url.lower().startswith("http"):
        # It is a real web URL
        r = requests.get(url)
        r.raise_for_status()
        with open(path, "wb") as f:
            f.write(r.content)
    else:
        # It's a local file path → copy it
        shutil.copy(url, path)


    download(req.kb_url, kb_path)
    download(req.fi_url, fi_path)

    from server.pipeline.end_to_end_pipeline import DFMEAEndToEndPipeline

    pipeline = DFMEAEndToEndPipeline(kb_path=kb_path, fi_path=fi_path, query=req.query)
    output_path = pipeline.run()

    filename = os.path.basename(output_path)
    return {
        "status": "success",
        "output_file_url": f"http://localhost:8000/files/{filename}"
    }
