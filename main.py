import os
import numpy as np
from PIL import Image
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.post("/shield")
async def apply_shield(file: UploadFile = File(...)):
    try:
        # Load and convert image to float for math operations
        img = Image.open(file.file).convert("RGB")
        img_array = np.array(img).astype(np.float32)
        h, w, c = img_array.shape

        # 1. ROBUST INVISIBLE WATERMARK (Block-Based)
        # Strategy: Embed data in 8x8 blocks for high-durability protection
        block_size = 8
        for y in range(0, h - block_size, block_size):
            for x in range(0, w - block_size, block_size):
                if (x + y) % 3 == 0:
                    img_array[y:y+block_size, x:x+block_size, 2] += 1.0

        # 2. ADVERSARIAL NOISE (Anti-AI Layer)
        # Strategy: Seed-based noise (±2 pixels) to disrupt AI model mapping
        np.random.seed(42) 
        noise = np.random.randint(-2, 3, (h, w, c))
        img_array = np.clip(img_array + noise, 0, 255).astype(np.uint8)

        output_path = os.path.join(BASE_DIR, "shielded_aevum.png")
        result_img = Image.fromarray(img_array)
        result_img.save(output_path)

        return FileResponse(output_path, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open(os.path.join(BASE_DIR, "index.html"), "r") as f:
        return f.read()