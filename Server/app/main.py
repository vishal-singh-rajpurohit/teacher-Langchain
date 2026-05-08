from fastapi import FastAPI

app = FastAPI()

@app.get('/test')
def root():
    return "Hii"