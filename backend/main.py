from fastapi import FastAPI
from presentation.routes.auth_routes import authRouter

app = FastAPI(debug=True)

app.include_router(authRouter, prefix="/api", tags=["Auth"])
