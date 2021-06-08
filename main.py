from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

# lesson 2


@app.get("/posts")
async def getPosts():
    return {"data": "getting posts"}
