from cerberus import Validator

from apps.task_system.helpers.enums_tasks_state import ENUMS_TASK_STATE_MAP


class ManageTaskStateValidate:

    schema = {
        "status": {
            "type": "string",
            "required": True,
            "maxlength": 8,
            "allowed": list(dict(ENUMS_TASK_STATE_MAP).keys()),
        },
    }

    def __init__(self, data):
        self.validator = Validator()
        self.data = data
        self.schema = self.__class__.schema

    def validate(self):
        return self.validator.validate(self.data, self.schema)

    def errors(self):
        return self.validator.errors
