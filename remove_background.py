import aiohttp
import base64
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from io import BytesIO
import logging
from PIL import Image
from rembg import remove
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
	logger.info("Starting API...")
	yield
	logger.info("Shutting down API...")

app = FastAPI(
	title="Rembg API",
	description="API for background removal",
	version="1.0.0",
	lifespan=lifespan
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
	return templates.TemplateResponse("index.html", {"request": request})

@app.post("/rembg")
async def remove_bg(request: Request):
	"""
	Remove background from image at given URL
	
	Args:
		image_url: URL of the image to process
		
	Returns:
		Dict with base64 encoded image without background
	"""
	data = await request.json()
	image_url = data.get("image_url")
	logger.info(f"Removing background from {image_url}")
	try:
		# Download the image
		async with aiohttp.ClientSession() as session:
			async with session.get(image_url) as response:
				image_data = await response.read()
		
		# Process with rembg
		input_image = Image.open(BytesIO(image_data))
		output_image = remove(input_image)
		
		# Convert to base64 for transfer
		buffered = BytesIO()
		output_image.save(buffered, format="PNG")
		img_str = base64.b64encode(buffered.getvalue()).decode()
		logger.info(f"{img_str}")
		return {"status": "success", "image_base64": img_str}
	except Exception as e:
		logger.error(f"Error removing background: {e}")
		return {"status": "error", "message": str(e)}

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
	"""Global exception handler for FastAPI app."""
	logger.error(f"Error occurred: {exc}")
	return JSONResponse(
		status_code=500,
		content={"detail": str(exc)}
	)

if __name__ == "__main__":
	uvicorn.run("remove_background:app", host="0.0.0.0", port=8008, reload=True)