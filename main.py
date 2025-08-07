# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from server.pipeline.end_to_end_pipeline import DFMEAEndToEndPipeline

# app = FastAPI()

# # Enable CORS (for later React UI)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/")
# def read_root():
#     return {"message": "DFMEA GenAI platform is alive!"}

# @app.post("/run_dfmea")
# def run_dfmea():
#     kb_path = "server/sample_files/dfmea_knowledge_bank_3.csv"
#     fi_path = "server/sample_files/field_reported_issues_3.xlsx"
#     query = "Generate DFMEA entries for recent field failures"

#     pipeline = DFMEAEndToEndPipeline(kb_path=kb_path, fi_path=fi_path, query=query, top_k=100)
#     output_path = pipeline.run()

#     return {
#         "status": "success",
#         "message": "DFMEA run complete",
#         "output_file": output_path
#     }


from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import Request,FastAPI
from pydantic import BaseModel
import requests
import os 
from server.pipeline.end_to_end_pipeline import DFMEAEndToEndPipeline
import shutil

app = FastAPI()

# Enable CORS (for later React UI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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

    

    pipeline = DFMEAEndToEndPipeline(kb_path=kb_path, fi_path=fi_path, query=req.query)
    output_path = pipeline.run()

    filename = os.path.basename(output_path)
    return {
        "status": "success",
        "output_file_url": f"http://localhost:8000/files/{filename}"
    }
