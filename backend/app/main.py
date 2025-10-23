from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Firebase Admin SDK
cred_path = os.path.join(os.path.dirname(__file__), '..', '..', 'globaldashboard-4598e-firebase-adminsdk-fbsvc-8820178d65.json')
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

# Create FastAPI app
app = FastAPI(
    title="DataGate API",
    description="File upload and management system with Firebase Authentication",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from app.routes import files, admin
app.include_router(files.router, prefix="/api/files", tags=["files"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])

@app.get("/")
async def root():
    return {"message": "DataGate API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "DataGate API"}
