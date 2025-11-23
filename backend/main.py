from fastapi import FastAPI
from presentation.routes.auth_routes import authRouter
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(debug=True)
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(authRouter, prefix="/api", tags=["Auth"])
