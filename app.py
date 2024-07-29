from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
from mercadona.ticket_parser.parser import build_ticket
from typing import List
import logging

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Product(BaseModel):
    producto: str
    cantidad: int
    precio: float
    timestamp: datetime

class AuthorInfo(BaseModel):
    name: str
    email: str
    bio: str

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/upload_ticket", response_model=List[Product])
def upload_ticket(file: UploadFile = File(...)):
    try:
        # Read file content
        logger.info("File content read successfully.")

        # Call build_ticket to process the file content
        ticket_data = build_ticket(file.file)
        logger.info("Ticket data processed successfully.")

        # Transform the output to return a list of Product objects
        products = [
            Product(
                producto=product.name,
                cantidad=product.quantity,
                precio=product.price,
                timestamp=ticket_data.bought_at
            )
            for product in ticket_data.products
        ]

        return products
    except Exception as e:
        logger.error(f"Error processing ticket: {e}")
        raise HTTPException(status_code=500, detail="Error processing ticket.")

@app.get("/about", response_model=list[AuthorInfo])
async def get_about_info():
    author_info = AuthorInfo(
        name="Nubecita de Mis amigos",
        email="hi@nubecitas.dev",
        bio="Just friends coding."
    )
    return [author_info]

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."},
    )
