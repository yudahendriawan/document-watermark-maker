import io
import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from watermarker import add_watermark

app = FastAPI(title="Local Document Watermark Server")

# Izinkan CORS jika ada kebutuhan integrasi
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tentukan path untuk folder statis dan template
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Buat folder static jika belum ada
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

# Mount folder static untuk menyajikan file CSS dan JS
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
async def get_index():
    index_path = os.path.join(TEMPLATES_DIR, "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="index.html tidak ditemukan")
    return FileResponse(index_path)

@app.post("/api/watermark")
async def api_watermark(
    file: UploadFile = File(...),
    text: str = Form(...),
    opacity: int = Form(30),
    angle: int = Form(30),
    scale: float = Form(0.035),
    grid: bool = Form(True),
    spacing: int = Form(150),
    color: str = Form("#ffffff")
):
    try:
        # Baca isi file gambar ke memori
        contents = await file.read()
        image_input = io.BytesIO(contents)
        
        # Jalankan fungsi watermark di memori
        result_img = add_watermark(
            image_path=image_input,
            text=text,
            output_path=None,  # Jangan simpan ke file, simpan ke memori
            opacity=opacity,
            angle=angle,
            scale=scale,
            grid=grid,
            spacing=spacing,
            color_hex=color
        )
        
        # Simpan hasil pemrosesan gambar ke stream byte
        img_byte_arr = io.BytesIO()
        
        # Tentukan format keluaran berdasarkan format asli atau default ke PNG
        file_ext = os.path.splitext(file.filename or "")[1].lower()
        if file_ext in ['.jpg', '.jpeg']:
            save_format = "JPEG"
            media_type = "image/jpeg"
        else:
            save_format = "PNG"
            media_type = "image/png"
            
        result_img.save(img_byte_arr, format=save_format)
        img_byte_arr.seek(0)
        
        return StreamingResponse(img_byte_arr, media_type=media_type)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal memproses gambar: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
