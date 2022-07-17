from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from asyncio import create_task

from vintt4.VinttWatcher import VinttWatch

app:FastAPI=FastAPI()

async def startwatcher():
    VinttWatch(
        configpath="vinttconfig.yml",
        timefile="timefile.yml"
    )

@app.on_event("startup")
async def serverstart():
    create_task(startwatcher())

# --- static ---
app.mount("/",
    StaticFiles(
        directory="../vintt3-web/build",
        html=True
    ),
    name="root"
)
