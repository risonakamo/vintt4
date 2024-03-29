from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.concurrency import run_in_threadpool
from asyncio import ensure_future
from loguru import logger
from subprocess import Popen
from os import system
from os.path import dirname,realpath,join

from vintt4.VinttWatcher import VinttWatch,DEFAULT_WATCH
import vintt4.log_control

from typing import Optional
from vintt4.types.vintt_watch_types import CurrentWatch
from vintt4.types.web_api_types import NewCategoryReq, SetCategoryReq
from vintt4.vintt_config import addCategoryToConfig

HERE=dirname(realpath(__file__))
TIMEFILE:str=join(HERE,"timefile.yml")
VINTTCONFIG:str=join(HERE,"vinttconfig.yml")

app:FastAPI=FastAPI()
vinttwatch:Optional[VinttWatch]=None

def dowatch():
    """begin watching"""

    global vinttwatch
    vinttwatch=VinttWatch(
        configpath=VINTTCONFIG,
        timefile=TIMEFILE
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

@app.get("/open-config")
def openconfig()->None:
    """open config with system default program"""

    system(f"start {VINTTCONFIG}")

@app.get("/open-timefile")
def opentimefile()->None:
    """open timefile with system default program"""

    system(f"start {TIMEFILE}")

@app.post("/new-category")
def newcategory(request:NewCategoryReq)->None:
    """add new category"""

    if not vinttwatch or not vinttwatch.trackProcess:
        logger.error("no watch")
        raise HTTPException(500,detail="no watch")

    vinttwatch.addCategory(request.categoryName)

    addCategoryToConfig(
        path=VINTTCONFIG,
        program=vinttwatch.trackProcess,
        category=request.categoryName
    )



# --- static ---
app.mount("/",
    StaticFiles(
        directory="../vintt3-web/build",
        html=True
    ),
    name="root"
)

Popen("chrome --window-size=500,500 --new-window http://localhost:4301")
logger.info("server running: http://localhost:4301")