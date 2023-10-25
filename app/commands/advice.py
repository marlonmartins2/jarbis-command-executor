import requests

from datetime import datetime

from database.controllers.commands import Commands


def advice_process(process, command_id):
    """
    Process weather command.

    - **process**: Processed text.
    - **command_id**: Command ID.
    """

    response = requests.get(
        f"https://api.adviceslip.com/advice"
    )
    
    if response.status_code != 200:
        return False

    command = {
        "status": "completed",
        "advice": response.json()["slip"]["advice"],
        "updated_at": datetime.now(),
    }

    Commands.update_command(command_id, command)

    return command
