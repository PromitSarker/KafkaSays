from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import random, json, os

app = FastAPI()

File = "text.json"

def load_data():
    if os.path.exists(File):
        with open(File, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(File, "w") as f:
        json.dump(data, f)

class Item(BaseModel):
    id: int
    text: str
    category: str

@app.get("/quote")
def get_random_quote(category: Optional[str] = None):
    quotes = load_data()
    if category:
        filtered = [q for q in quotes if q["category"].lower() == category.lower()]
        if not filtered:
            raise HTTPException(status_code=404, detail="No quotes found in this category")
        return random.choice(filtered)
    return random.choice(quotes)
   

@app.get("/quotes")
def all_quotes():
    return load_data()

@app.post("/quote")
def add_quote(quote: Item):
    quotes = load_data()
    new_id = max([q["id"] for q in quotes], default=0) + 1
    new_quote = {"id": new_id, **quote.dict()}
    quotes.append(new_quote)
    save_data(quotes)
    return new_quote

@app.delete("/quote/{quote_id}")
def delete_quote(quote_id: int):
    quotes = load_data()
    for q in quotes:
        if q["id"] == quote_id:
            quotes.remove(q)
            save_data(quotes)
            return {"message": "Quote deleted"}
    raise HTTPException(status_code=404, detail="Quote not found")
    