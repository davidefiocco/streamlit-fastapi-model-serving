from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    number: int


app = FastAPI(title="Sum one",
              description="Get a number, add one to it",
              version="0.1.0",
              )


@app.post("/compute")
async def compute(input: Item):
    return {'result': input.number + 1}
