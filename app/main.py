from __future__ import annotations

import io
from typing import Any

import pandas as pd
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from app.sentiment import SentimentService

APP_TITLE: str = "Análisis de Sentimiento (Excel)"
INPUT_COLUMN: str = "Valoración"
OUTPUT_COLUMN: str = "Tipo de valoración"

app: FastAPI = FastAPI(title=APP_TITLE)
templates: Jinja2Templates = Jinja2Templates(directory="app/templates")

sentiment_service: SentimentService = SentimentService()


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> Any:
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": APP_TITLE, "input_column": INPUT_COLUMN, "output_column": OUTPUT_COLUMN},
    )


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)) -> StreamingResponse:
    filename: str = file.filename or "input.xlsx"
    if not filename.lower().endswith(".xlsx"):
        raise_http_400("El archivo debe ser .xlsx")

    content: bytes = await file.read()
    if len(content) == 0:
        raise_http_400("El archivo está vacío")

    try:
        df: pd.DataFrame = pd.read_excel(io.BytesIO(content), engine="openpyxl")
    except Exception:
        raise_http_400("No se pudo leer el Excel. Verifica que sea un .xlsx válido")

    if INPUT_COLUMN not in df.columns:
        raise_http_400(f'No existe la columna "{INPUT_COLUMN}" en el Excel')

    def classify(value: Any) -> str:
        if pd.isna(value):
            return "Valoración neutra"
        return sentiment_service.analyze(str(value)).tipo_valoracion

    df[OUTPUT_COLUMN] = df[INPUT_COLUMN].apply(classify)

    output_stream: io.BytesIO = io.BytesIO()
    with pd.ExcelWriter(output_stream, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Resultado")
    output_stream.seek(0)

    out_name: str = filename.replace(".xlsx", "") + "_analizado.xlsx"
    headers = {"Content-Disposition": f'attachment; filename="{out_name}"'}

    return StreamingResponse(
        output_stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers,
    )


def raise_http_400(message: str) -> None:
    from fastapi import HTTPException
    raise HTTPException(status_code=400, detail=message)