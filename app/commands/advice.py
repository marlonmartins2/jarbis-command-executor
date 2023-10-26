import requests

from datetime import datetime

from database.controllers.commands import Commands
from database.controllers.advice import Advice


def advice_process(process, command_id):
    """
    Process weather command.

    - **process**: Processed text.
    - **command_id**: Command ID.
    """

    advice = Advice.get_advice()


    command = {
        "status": "completed",
        "advice": advice["advice"],
        "updated_at": datetime.now(),
    }

    Commands.update_command(command_id, command)

    return command
