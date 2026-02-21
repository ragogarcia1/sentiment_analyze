# Sentiment Analyze
 https://sentiment-analyze-86473661674.europe-west1.run.app/

## Overview
Sentiment Analyze es una aplicación web con FastAPI que clasifica el sentimiento de texto en español a partir de archivos Excel.

La aplicación resuelve un caso de uso de procesamiento por lotes: el usuario sube un archivo `.xlsx` con una columna `Valoración`, y el servicio devuelve un nuevo `.xlsx` con una columna adicional de etiqueta de sentimiento (`Tipo de valoración`).

## Features
- Carga y procesamiento de archivos `.xlsx` desde una interfaz web.
- Validación de tipo de archivo, archivos vacíos y columna de entrada requerida.
- Análisis de sentimiento en español usando `pysentimiento`.
- Generación de un nuevo Excel con etiquetas de salida y descarga automática.
- Clasificación de valores vacíos/nulos como sentimiento neutro.
- Carga diferida del modelo NLP para reducir el tiempo de inicio del proceso.

## Tech Stack
| Categoría | Herramientas |
|---|---|
| Lenguaje | Python 3.11 |
| Framework API | FastAPI |
| Servidor ASGI | Uvicorn |
| Plantillas | Jinja2 |
| Frontend | HTML + Tailwind CSS (CDN) + JavaScript vanilla |
| Procesamiento de datos | pandas + openpyxl |
| NLP / ML | pysentimiento, transformers, torch, sentencepiece |
| Contenerización | Docker |

## Architecture
El proyecto sigue una arquitectura monolítica en capas de tamaño pequeño:

- Capa de presentación: rutas FastAPI y plantilla HTML renderizada con Jinja2.
- Capa de aplicación/servicio: `SentimentService` encapsula la carga del modelo y el mapeo de etiquetas.
- Capa de procesamiento de datos: pandas lee/escribe archivos Excel y transforma columnas.

### Component Interaction
1. El usuario abre `/` y sube un archivo Excel.
2. `POST /analyze` valida la entrada y carga el libro con pandas.
3. Cada valor de `Valoración` se envía a `SentimentService.analyze`.
4. El servicio mapea la salida del modelo (`POS`, `NEG`, `NEU`) a etiquetas en español.
5. La API escribe un nuevo libro y lo devuelve en streaming como descarga.

## Project Structure
```text
.
├─ app/
│  ├─ main.py                # App FastAPI, rutas y flujo de procesamiento Excel
│  ├─ sentiment.py           # Servicio de sentimiento y mapeo de etiquetas
│  └─ templates/
│     └─ index.html          # Interfaz de carga y flujo de descarga
├─ requirements.txt          # Dependencias Python
├─ Dockerfile                # Build de contenedor y comando de ejecución
├─ .gitignore                # Exclusiones de Git
└─ .dockerignore             # Exclusiones del contexto de build Docker
```

## Getting Started

### Prerequisites
- Python 3.11
- `pip`
- Acceso a Internet en la primera ejecución para descargar artefactos del modelo NLP (cache de Hugging Face)

### Installation
```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
```

### Configuration
El código de la aplicación no define variables de entorno obligatorias personalizadas.

Valores por defecto de runtime/contenedor definidos en `Dockerfile`:

| Variable | Propósito | Valor por defecto |
|---|---|---|
| `PORT` | Puerto de Uvicorn en el contenedor | `8080` |
| `HF_HOME` | Directorio de cache de Hugging Face | `/tmp/hf` |
| `TRANSFORMERS_CACHE` | Directorio de cache de Transformers | `/tmp/hf` |
| `TOKENIZERS_PARALLELISM` | Comportamiento de paralelismo de tokenizers | `false` |

### Running the Project
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

Luego abre: `http://localhost:8080`

## Usage
### Flujo Web
1. Abre la página principal.
2. Sube un archivo `.xlsx` que contenga la columna `Valoración`.
3. Envía el formulario.
4. Descarga el archivo procesado (`*_analizado.xlsx`) con la nueva columna `Tipo de valoración`.

### API Endpoints
| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/` | Renderiza la página de carga |
| `POST` | `/analyze` | Recibe un Excel y devuelve el Excel procesado |

### Reglas de Entrada/Salida
- El archivo de entrada debe ser `.xlsx`.
- Los archivos vacíos son rechazados.
- Si falta la columna `Valoración`, se rechaza el archivo.
- Los valores vacíos/nulos se clasifican como `Valoración neutra`.

## Testing
No hay pruebas automatizadas incluidas en el repositorio.

## Deployment
### Docker
Construir imagen:
```bash
docker build -t sentiment-analyze .
```

Ejecutar contenedor:
```bash
docker run --rm -p 8080:8080 -e PORT=8080 sentiment-analyze
```

El contenedor inicia Uvicorn con:
```bash
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}
```

## Contributing
1. Crea una rama de feature.
2. Mantén los cambios enfocados y pequeños.
3. Agrega pruebas cuando aplique.
4. Abre un pull request con una descripción clara y pasos de validación.

## License
No license specified.

## Assumptions / Missing Information
- No existe configuración de pipeline CI/CD en el repositorio.
- No existe `.env.example` ni un contrato explícito de variables de entorno.
- No hay suite de pruebas automatizadas.
- El repositorio no incluye una estrategia de versionado/pinning de modelos más allá de las versiones de dependencias.
