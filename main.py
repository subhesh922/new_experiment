# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# # Allow frontend to call API (we’ll connect React later)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # You can restrict this to localhost later
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.get("/")
# def read_root():
#     return {"message": "DFMEA GenAI platform is alive!"}


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.pipeline.end_to_end_pipeline import DFMEAEndToEndPipeline

app = FastAPI()

# Enable CORS (for later React UI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "DFMEA GenAI platform is alive!"}

@app.post("/run_dfmea")
def run_dfmea():
    kb_path = "server/sample_files/dfmea_knowledge_bank_3.csv"
    fi_path = "server/sample_files/field_reported_issues_3.xlsx"
    query = "Generate DFMEA entries for recent field failures"

    pipeline = DFMEAEndToEndPipeline(kb_path=kb_path, fi_path=fi_path, query=query, top_k=100)
    output_path = pipeline.run()

    return {
        "status": "success",
        "message": "DFMEA run complete",
        "output_file": output_path
    }
