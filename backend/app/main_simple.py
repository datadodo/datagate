from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
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

@app.get("/")
async def root():
    return {"message": "DataGate API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "DataGate API"}

@app.get("/api/test")
async def test():
    return {"message": "Test endpoint working"}
