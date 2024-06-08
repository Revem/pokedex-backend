import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def oi_eu_sou_programador() -> str:
  return "API Testing."

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8001)