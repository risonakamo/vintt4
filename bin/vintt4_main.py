from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.concurrency import run_in_threadpool
from asyncio import ensure_future

from vintt4.VinttWatcher import VinttWatch

from typing import Optional

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

@app.get("/hello")
def test():
    print("?")
    if not vinttwatch:
        print("no watch")
        return

    print(vinttwatch.getCurrentWatch())
    return "adad"

# --- static ---
app.mount("/",
    StaticFiles(
        directory="../vintt3-web/build",
        html=True
    ),
    name="root"
)
