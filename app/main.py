import settings

from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware

from version import __version__

from routers.voice import voice_router


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    debug=settings.DEBUG,
    version=__version__,
    contact={
        "name": "Marlon Martins",
        "url": "https://github.com/marlonmartins2",
        "email": "marlon.azevedo.m@gmail.com",
    },
    license_info={
        "name": "Copyright",
        "url": "https://github.com/marlonmartins2/jarbis-command-executor/blob/master/LICENSE",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(voice_router)


@app.get("/health_check")
def health_check():
    """
    Check if API is running.
    """
    return Response(status_code=status.HTTP_204_NO_CONTENT)
