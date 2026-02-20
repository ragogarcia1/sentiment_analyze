from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SentimentResult:
    tipo_valoracion: str


class SentimentService:
    _analyzer = None

    def _load(self) -> None:
        if SentimentService._analyzer is not None:
            return

        from pysentimiento import create_analyzer  # type: ignore
        SentimentService._analyzer = create_analyzer(task="sentiment", lang="es")

    def analyze(self, text: Optional[str]) -> SentimentResult:
        if text is None:
            return SentimentResult(tipo_valoracion="Valoración neutra")

        cleaned_text: str = str(text).strip()
        if cleaned_text == "":
            return SentimentResult(tipo_valoracion="Valoración neutra")

        self._load()

        prediction = SentimentService._analyzer.predict(cleaned_text)  # POS/NEG/NEU
        label: str = str(prediction.output).upper()

        if label == "POS":
            return SentimentResult(tipo_valoracion="Valoración positiva")
        if label == "NEG":
            return SentimentResult(tipo_valoracion="Valoración negativa")
        return SentimentResult(tipo_valoracion="Valoración neutra")