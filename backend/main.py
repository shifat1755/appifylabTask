from fastapi import FastAPI

app = FastAPI(debug=True)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
