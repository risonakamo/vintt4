from fastapi import FastAPI,staticfiles
from fastapi.staticfiles import StaticFiles

app:FastAPI=FastAPI()

# --- static ---
app.mount("/",
    StaticFiles(
        directory="../vintt3-web/build",
        html=True
    ),
    name="root"
)