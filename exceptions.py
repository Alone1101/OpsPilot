class OpsPilotError(Exception):
    pass

class OrderNotFoundError(OpsPilotError):
    pass

class InvalidOrderActionError(OpsPilotError):
    pass

class UnkownToolError(OpsPilotError):
    pass