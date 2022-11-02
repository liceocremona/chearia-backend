from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from routers import board, resources
from docs import tags_metadata_docs, description_docs



app = FastAPI(
    openapi_tags=tags_metadata_docs,
    title="Progetto CHeArIA",
    description=description_docs,
    version="1.0",
    contact={
        "url": "https://progettochearia.it"
    },
    license_info={
        "name": "GNU General Public License v3.0",
        "url": "https://raw.githubusercontent.com/liceocremona/chearia-backend/main/LICENSE"
    }
    )

origins=["https://progettochearia.it",
 "https://web.progettochearia.it",
 "https://admin.progettochearia.it"]
app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    board.router,
    prefix="/board",
)
app.include_router(
    resources.router,
    prefix="/resources",
)


@app.get("/", response_class=RedirectResponse, status_code=302, include_in_schema=False)
async def root():
    return "https://api.progettochearia.it/v1/docs"

