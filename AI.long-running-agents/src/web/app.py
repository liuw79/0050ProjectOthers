from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .api import router

app = FastAPI(title="长运行代理 Dashboard")
app.include_router(router, prefix="/api")

# 挂载静态文件
app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/health")
def health():
    return {"status": "ok"}
