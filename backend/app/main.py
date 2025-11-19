from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Firebase Admin SDK
import json
import base64

# Try to get service account from environment variable first
service_account_json = os.getenv('FIREBASE_SERVICE_ACCOUNT_JSON')
if service_account_json:
    try:
        # Decode base64 encoded service account JSON
        service_account_data = json.loads(base64.b64decode(service_account_json).decode('utf-8'))
        cred = credentials.Certificate(service_account_data)
        firebase_admin.initialize_app(cred)
        print("Firebase initialized from environment variable")
    except Exception as e:
        print(f"Failed to initialize Firebase from environment: {e}")
        # Try fallback to file
        try:
            cred_path = '/app/globaldashboard-4598e-firebase-adminsdk-fbsvc-8820178d65.json'
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            print("Firebase initialized from file")
        except Exception as e2:
            print(f"Failed to initialize Firebase from file: {e2}")
            print("Continuing without Firebase initialization")
else:
    # Fallback to file (for local development)
    try:
        cred_path = '/app/globaldashboard-4598e-firebase-adminsdk-fbsvc-8820178d65.json'
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        print("Firebase initialized from file")
    except Exception as e:
        print(f"Failed to initialize Firebase from file: {e}")
        print("Continuing without Firebase initialization")

# Create FastAPI app
# Note: FastAPI/Starlette handles large file uploads by streaming, so no explicit size limit needed
# The main constraints are timeouts, which we configure at the uvicorn level
app = FastAPI(
    title="DataGate API",
    description="File upload and management system with Firebase Authentication",
    version="1.0.0"
)

# Configure CORS
allowed_origins = [
    "https://datagate.web.app",
    "https://globaldashboard-4598e.web.app",
    "http://localhost:3000",  # For local development
    "http://localhost:5173",  # For Vite dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
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
