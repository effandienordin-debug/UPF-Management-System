from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import auth, meeting_rooms, vehicles, visitors, maintenance, inventory, parking, stationery, equipment
from .database import engine, Base

# Create database tables (not recommended for production, use migrations)
# Base.metadata.create_all(bind=engine)

from fastapi.staticfiles import StaticFiles
import os

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("server.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="UPF Integrated Facility, Resource, Visitor & Maintenance Management System API"
)

# Ensure static directory exists
static_dir = os.path.join(os.getcwd(), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

# Mount static files
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with streamlit app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(meeting_rooms.router, prefix="/meeting-rooms", tags=["Meeting Rooms"])
app.include_router(vehicles.router, prefix="/vehicles", tags=["Vehicles"])
app.include_router(visitors.router, prefix="/visitors", tags=["Visitors"])
app.include_router(maintenance.router, prefix="/maintenance", tags=["Maintenance"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
app.include_router(parking.router, prefix="/parking", tags=["Parking"])
app.include_router(stationery.router, prefix="/stationery", tags=["Stationery POS"])
app.include_router(equipment.router, prefix="/equipment", tags=["Equipment Borrowing"])

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}
