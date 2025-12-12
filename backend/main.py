import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uuid
import os
import shutil
import asyncio
from concurrent.futures import ThreadPoolExecutor
from pipeline.pipeline import run_pipeline
from models import LocationRequest
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# For better Async
executor = ThreadPoolExecutor(max_workers=8)

# BASE TMP FOLDER
TMP_BASE = "/workspace/tmp/requests"

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # or ["http://localhost:5500"] if you want to restrict
    allow_credentials=True,
    allow_methods=["*"],     # Allow POST, GET, OPTIONS
    allow_headers=["*"],
)

# Message for errror
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "message": "Invalid Request - Error Messaging to be Improved! Maybe You did not send lon/lat as JSON Body Req",
            # "details": exc.errors()
        }
    )

# Only three functional routes
# GET:  /health     => return { status: "ok" }
# GET:  /           => return { "message": "Welcome to My Flood mApp" }
# POST: /           => req: lat/lon; return {...}
@app.get("/")
async def root():
    return {"message": "Welcome to My Flood mApp"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/")
async def process(req: LocationRequest):
    # Early exit for no lon/lat
    if req.lat is None or req.lon is None:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Invalid Request - Error Messaging to be Improved! Maybe You did not send lon/lat as JSON Body Req",
            }
        )
    
    request_id = str(uuid.uuid4())
    req_dir = f"{TMP_BASE}/{request_id}"
    os.makedirs(req_dir, exist_ok=True)
    
    try:
        result = await asyncio.get_event_loop().run_in_executor(
            executor,
            run_pipeline,
            req.lat,
            req.lon,
            req_dir
        )
        
        return result;
    except Exception as e:
        print(f"Error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Internal Server Error - Processing Failed",
            }
        )

    finally:
        shutil.rmtree(req_dir, ignore_errors=True)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
