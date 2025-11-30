from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from presentation.routes.auth_routes import authRouter
from presentation.routes.comment_routes import commentRouter
from presentation.routes.like_routes import likeRouter
from presentation.routes.media_routes import mediaRouter
from presentation.routes.notification_routes import notificationRouter
from presentation.routes.post_routes import postRouter
from presentation.routes.user_routes import userRouter

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

# Mount static files directory for uploaded images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Register routers
app.include_router(authRouter, prefix="/api", tags=["Auth"])
app.include_router(postRouter, prefix="/api", tags=["Posts"])
app.include_router(commentRouter, prefix="/api", tags=["Comments"])
app.include_router(likeRouter, prefix="/api", tags=["Likes"])
app.include_router(notificationRouter, prefix="/api", tags=["Notifications"])
app.include_router(userRouter, prefix="/api", tags=["User"])
app.include_router(mediaRouter, prefix="/api", tags=["Media"])
# app.include_router(websocketRouter, prefix="/api", tags=["WebSocket"])
