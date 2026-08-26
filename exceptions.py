class OpsPilotError(Exception):
    pass

class OrderNotFoundError(OpsPilotError):
    pass

class InvalidOrderActionError(OpsPilotError):
    pass

class UnkownToolError(OpsPilotError):
    pass

class InvalidToolArgumentsError(OpsPilotError):
    pass

class EscalationRequiredError(OpsPilotError):
    pass

class LLMError(OpsPilotError):
    pass

class LLMUnavailableError(LLMError):
    pass

class LLMResponseError(LLMError):
    pass