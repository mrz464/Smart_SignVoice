from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.translate import router as translate_router

app = FastAPI(
    title="BicaraUntukku API",
    description="REST API untuk terjemah bahasa isyarat BISINDO",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(translate_router, tags=["Translation"])

@app.get("/")
def root():
    return {"message": "BicaraUntukku API is running!"}

@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}