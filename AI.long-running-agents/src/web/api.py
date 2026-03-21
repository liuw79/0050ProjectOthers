from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

router = APIRouter()

@router.get("/status")
def get_status():
    return {
        "features": {"total": 0, "completed": 0},
        "git": {"initialized": True},
        "progress": "Ready"
    }

@router.get("/features")
def get_features():
    return []

@router.websocket("/logs")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.receive_text()
            await websocket.send_json({"type": "log", "message": "Test log"})
    except WebSocketDisconnect:
        pass
