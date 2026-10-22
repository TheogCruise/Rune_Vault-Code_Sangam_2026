from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# @app.get("/")
# def home():
#     return {"message": "Hello world"}



@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def something():

    return "<h1>This is awsome</h1>"