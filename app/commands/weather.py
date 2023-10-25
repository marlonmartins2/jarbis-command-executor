import requests

import settings

from datetime import datetime

from database.controllers.commands import Commands


def weather_process(process, command_id):
    """
    Process weather command.

    - **process**: Processed text.
    - **command_id**: Command ID.
    """
    if not "LOC" in [entity.label_ for entity in process.ents]:
        return False

    location = [entity.text for entity in process.ents if entity.label_ == "LOC"][0]

    response = requests.get(
        f"{settings.WEATHER_API_URL}/weather?key={settings.WEATHER_API_KEY}&city_name={location}"
    )
    
    if response.status_code != 200:
        return False

    payload = response.json()["results"]

    forecast = payload["forecast"][0]

    message_return = f"Previsão do tempo {location}, tempo {payload['description']} temperatura mínima {forecast['min']} graus, temperatura máxima {forecast['max']} graus, data da previsão dia {forecast['date']}"

    command = {
        "status": "completed",
        "location": location,
        "description": payload["description"],
        "min_temp": forecast["min"],
        "max_temp": forecast["max"],
        "date": forecast["date"],
        "message": message_return,
        "updated_at": datetime.now(),
    }

    Commands.update_command(command_id, command)

    return command