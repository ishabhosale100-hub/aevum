import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
import numpy as np

app = FastAPI()

# Important: Get the directory where main.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Mount static files for your index.html
app.mount("/static", StaticFiles(directory=BASE_DIR, html=True), name="static")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.post("/shield")
async def apply_shield(file: UploadFile = File(...)):
    # 1. Load the uploaded image
    img = Image.open(file.file).convert("RGB")
    img_array = np.array(img)

    # 2. Forensic Logic: Apply Invisible Watermark (Pre-Shield)
    # Simple example: Modifying a specific bit in the blue channel
    shielded_array = img_array.copy()
    shielded_array[:, :, 2] = (shielded_array[:, :, 2] // 2) * 2 + 1 

    # 3. Save the result in the current directory
    output_path = os.path.join(BASE_DIR, "shielded_result.png")
    shielded_img = Image.fromarray(shielded_array)
    shielded_img.save(output_path)

    return FileResponse(output_path)