class NotFoundError(Exception):
    def __init__(self, name: str):
        super().__init__(f"{name} not found")


class NotCreatedError(Exception):
    def __init__(self, name: str, error: str | None = None):
        super().__init__(f"{name} not created. {error}")


class NotUpdatedError(Exception):
    def __init__(self, name: str, error: str | None = None):
        super().__init__(f"{name} not updated. {error}")


class NotDeletedError(Exception):
    def __init__(self, name: str, error: str | None = None):
        super().__init__(f"{name} not deleted. {error}")
