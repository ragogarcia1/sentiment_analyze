from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


@dataclass(frozen=True)
class SentimentResult:
    tipo_valoracion: str


class SentimentService:
    _analyzer: Optional[SentimentIntensityAnalyzer] = None

    def _load(self) -> None:
        if SentimentService._analyzer is not None:
            return

        # Descarga el lexicón VADER si no está
        try:
            nltk.data.find("sentiment/vader_lexicon.zip")
        except LookupError:
            nltk.download("vader_lexicon")

        SentimentService._analyzer = SentimentIntensityAnalyzer()

    def analyze(self, text: Optional[str]) -> SentimentResult:
        if text is None:
            return SentimentResult(tipo_valoracion="Valoración neutra")

        cleaned_text: str = str(text).strip()
        if cleaned_text == "":
            return SentimentResult(tipo_valoracion="Valoración neutra")

        self._load()

        # VADER devuelve puntajes: neg, neu, pos y compound (-1 a 1)
        scores = SentimentService._analyzer.polarity_scores(cleaned_text)
        compound: float = float(scores.get("compound", 0.0))

        # Umbrales típicos VADER:
        # compound >= 0.05 -> positivo
        # compound <= -0.05 -> negativo
        # en medio -> neutro
        if compound >= 0.05:
            return SentimentResult(tipo_valoracion="Valoración positiva")
        if compound <= -0.05:
            return SentimentResult(tipo_valoracion="Valoración negativa")
        return SentimentResult(tipo_valoracion="Valoración neutra")
