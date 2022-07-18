from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.concurrency import run_in_threadpool
from asyncio import ensure_future
from loguru import logger
from subprocess import Popen

from vintt4.VinttWatcher import VinttWatch,DEFAULT_WATCH

from typing import Optional
from vintt4.types.vintt_watch_types import CurrentWatch
from vintt4.types.web_api_types import SetCategoryReq

app:FastAPI=FastAPI()
vinttwatch:Optional[VinttWatch]=None

def dowatch():
    """begin watching"""

    global vinttwatch
    vinttwatch=VinttWatch(
        configpath="vinttconfig.yml",
        timefile="timefile.yml"
    )
    vinttwatch.watchForProcess()

ensure_future(run_in_threadpool(dowatch))


# --- routes ---
@app.get("/get-watch")
def getwatch()->CurrentWatch:
    """get the current watch, or default if watch not started"""

    if not vinttwatch:
        logger.error("no watch")
        return DEFAULT_WATCH

    return vinttwatch.getCurrentWatch()

@app.post("/set-category")
def setcategory(setCategoryReq:SetCategoryReq)->None:
    """set category api"""

    if not vinttwatch:
        logger.error("no watch")
        return

    logger.info("setting category: {}",setCategoryReq.category)
    vinttwatch.changeCategory(setCategoryReq.category)


# --- static ---
app.mount("/",
    StaticFiles(
        directory="../vintt3-web/build",
        html=True
    ),
    name="root"
)

Popen("chrome --window-size=500,300 --new-window http://localhost:4301")