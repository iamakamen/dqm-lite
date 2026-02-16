from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import json

from db import get_all_runs, get_latest_run, get_run

app = FastAPI(title="DQM Lite API")
templates = Jinja2Templates(directory="templates")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/metrics/latest")
def metrics_latest():
    latest = get_latest_run()
    if not latest:
        raise HTTPException(status_code=404, detail="No runs found")
    return latest


@app.get("/metrics/history")
def metrics_history():
    return get_all_runs()


@app.get("/run/{run_id}")
def metrics_run(run_id: int):
    run = get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


# @app.get("/")
# def root():
#     return {"message": "DQM Lite API is running"}

@app.get("/")
def root():
    return RedirectResponse(url="/dashboard")


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    history = get_all_runs()
    history_json = json.dumps(history)
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "history_json": history_json,
        },
    )
