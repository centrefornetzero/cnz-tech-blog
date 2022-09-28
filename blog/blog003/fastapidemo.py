import uvicorn
import os
from fastapi import FastAPI
from model import Model

app = FastAPI()


@app.get("/")
def root():
  return {"message": "Welcome to the Centre For Net Zero Tech Blog"}


def predict(inputs):
  pred = Model.predict(inputs)
  return {"message": {"inputs": input, "prediction": pred}}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
