import requests

from datetime import datetime

from database.controllers.commands import Commands


def cep_process(process, command_id):
    """
    Process weather command.

    - **process**: Processed text.
    - **command_id**: Command ID.
    """

    cep = process.text.split("CEP")[1].strip()

    if not cep:
        return False

    cep = cep.replace("-", "")

    response = requests.get(f"https://brasilapi.com.br/api/cep/v2/{cep}/")

    message_return =f"CEP {cep}, localizado no estado {response.json()['state']} cidade {response.json()['city']}, bairro {response.json()['neighborhood']}, rua {response.json()['street']}"

    command = {
        "status": "completed",
        "cep": cep,
        "state": response.json()["state"],
        "city": response.json()["city"],
        "neighborhood": response.json()["neighborhood"],
        "street": response.json()["street"],
        "message": message_return,
        "updated_at": datetime.now(),
    }

    Commands.update_command(command_id, command)

    return command