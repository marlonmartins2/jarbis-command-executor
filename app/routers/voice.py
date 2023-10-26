import io

import settings

import speech_recognition as sr

from uuid import uuid4

from datetime import datetime

from gtts import gTTS

from fastapi import APIRouter, UploadFile, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, FileResponse

from commands import weather_process, cep_process, advice_process

from database.controllers.commands import Commands

voice_router = APIRouter(prefix="/voice", tags=["Voice"])

@voice_router.post("/speaker")
async def upload_audio(file: UploadFile):
    """
    Upload audio file and return command execute.

    - **file**: Audio file to be uploaded.
    """
    file_extension = file.filename.split(".")[-1]

    if file_extension not in ["wav",]:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"This file extension is not allowed, please upload a valid audio file.",
        )

    try:
        msg_return = ""

        recognizer = sr.Recognizer()

        audio_content = await file.read()

        audio_data = io.BytesIO(audio_content)    

        with sr.AudioFile(audio_data) as source:
            audio_data = recognizer.record(source, duration=10)

        content = recognizer.recognize_google(audio_data, language="pt-BR")

        process = settings.SPACY(content)

        command_payload = {
            "command_id": str(uuid4()),
            "command": "",
            "status": "processing",
            "created_at": datetime.now(),
        }

        if "tempo" in content:
            command_payload["command"] = "weather"
            Commands.insert_command(command_payload)

            weather = weather_process(process, command_payload.get("command_id"))

            msg_return = weather.get("message")

            if not weather:
                return HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Could not receive location on audio"
                )

        elif "conselho" in content:
            command_payload["command"] = "advice"
            Commands.insert_command(command_payload)

            advice = advice_process(process, command_payload.get("command_id"))

            msg_return = advice.get("advice")

        elif "CEP" in content:
            command_payload["command"] = "price"
            Commands.insert_command(command_payload)

            cep = cep_process(process, command_payload.get("command_id"))

            msg_return = cep.get("message")

            if not cep:
                return HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Could not receive cep on audio"
                )
        else:
            msg_return = "Não Tenho um comando para a sua solicitação, tente novamente"

        audio_return = gTTS(msg_return, lang="pt-br", tld="com.br")

        audio_return.save("output.mp3")

        return FileResponse(
            path="output.mp3",
            media_type="audio/mp3",
            filename="output.mp3",
        )

    except sr.UnknownValueError:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not understand audio")

    except sr.RequestError:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro to process request.")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error initializing recognizer")


@voice_router.get("/history")
def get_commands_history():
    """
    Get commands history.
    """
    commands = Commands.get_all_history()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(commands),
    )


@voice_router.get("/history/{command_id}")
def get_command_history(command_id: str):
    """
    Get command history by id.

    - **command_id**: Command id.
    """
    command = Commands.get_history_by_id(command_id)

    if not command:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Command {command_id} not found.",
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(command),
    )
