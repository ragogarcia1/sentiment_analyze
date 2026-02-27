# app/sentiment.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

MODEL_NAME: str = "pysentimiento/robertuito-sentiment-analysis"


@dataclass(frozen=True)
class SentimentResult:
    tipo_valoracion: str


class SentimentService:
    _analyzer = None

    def _load(self) -> None:
        if SentimentService._analyzer is not None:
            return

        from pysentimiento import create_analyzer  # type: ignore
        # Forzamos el modelo
        SentimentService._analyzer = create_analyzer(task="sentiment", lang="es", model_name=MODEL_NAME)

    def analyze(self, text: Optional[str]) -> SentimentResult:
        if text is None:
            return SentimentResult(tipo_valoracion="Valoración neutra")

        cleaned_text: str = str(text).strip()
        if cleaned_text == "":
            return SentimentResult(tipo_valoracion="Valoración neutra")

        self._load()

        prediction = SentimentService._analyzer.predict(cleaned_text)
        label: str = str(prediction.output).upper()

        if label == "POS":
            return SentimentResult(tipo_valoracion="Valoración positiva")
        if label == "NEG":
            return SentimentResult(tipo_valoracion="Valoración negativa")
        return SentimentResult(tipo_valoracion="Valoración neutra")
