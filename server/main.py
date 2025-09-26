from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = []


@app.post("/imu-data/")
async def imu_data(data: dict):
    # broadcast to all WebSocket clients
    to_remove = []
    for ws in clients:
        try:
            await ws.send_json(data)
        except:
            to_remove.append(ws)
    for ws in to_remove:
        clients.remove(ws)
    return {"status": "ok"}


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.append(ws)
    try:
        while True:
            await asyncio.sleep(1)  # keep connection alive
    except:
        if ws in clients:
            clients.remove(ws)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
