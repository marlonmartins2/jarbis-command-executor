from database import database, Collections


class Commands:

    @classmethod
    def get_all_history(cls):
        return list(database[Collections.COMMANDS].find(
            {},
            {"_id": 0}
        ))

    @classmethod
    def get_history_by_id(cls, command_id: str):
        return database[Collections.COMMANDS].find_one(
            {"command_id": command_id},
            {"_id": 0}
        )

    @classmethod
    def insert_command(cls, command: dict):
        database[Collections.COMMANDS].insert_one(command)

    @classmethod
    def update_command(cls, command_id, command: dict):
        database[Collections.COMMANDS].update_one(
            {"command_id": command_id},
            {"$set": command}
        )
