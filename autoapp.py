import uvicorn
from lain_backend.app import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
