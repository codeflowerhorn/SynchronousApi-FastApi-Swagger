import uvicorn 
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI() # fastapi object
id_counter = [0] # temporary id
books = {} # store our temporary data

app = FastAPI(
    title="Books API",
    description="A simple api for CRUD operations",
    version="1.0",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/book/{id}", status_code=status.HTTP_200_OK, tags=["Book"])
def get_book(id: int):
    data = None
    if id in books:
        data = {
            "message": "Get",
            "results": books[id]
        }
    else:
        data = {
            "message": "Item not found",
            "results": {}
        }

    return data

@app.get("/books", status_code=status.HTTP_200_OK, tags=["Book"])
def get_books():
    data = {
        "message": "Get",
        "results": books
    }

    return data

@app.post("/book", status_code=status.HTTP_201_CREATED, tags=["Book"])
def create_book(title: str, author: str, genre: str):
    id_counter[0] = id_counter[0] + 1 
    id = id_counter[0]
    books[id] = {
        "id": id,
        "title": title,
        "author": author,
        "genre": genre
    }

    data = {
        "message": "Created",
        "results": books[id]
    }

    return data

@app.put("/book/{id}", status_code=status.HTTP_200_OK, tags=["Book"])
def update_book(id: int, title: str = None, author: str = None, genre: str = None):
    data = None
    if id in books:
        if title != None:
            books[id]["title"] = title
        if author != None:
            books[id]["author"] = author
        if genre != None:
            books[id]["genre"] = genre
        data = {
            "message": "Updated",
            "results": books[id]
        }
    else:
        data = {
            "message": "Item not found",
            "results": {}
        }

    return data

@app.delete("/book/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Book"])
def delete_book(id: int):
    data = None
    if id in books: 
        results = books[id]
        del books[id]
        data = {
            "message": "Deleted",
            "results": results
        }
    else:
        data = {
            "message": "Item not found",
            "results": {}
        }

    return data

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
        