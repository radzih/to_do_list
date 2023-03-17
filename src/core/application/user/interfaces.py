from src.core.application.shared import interfaces


class DBGateway(
    interfaces.Commiter, interfaces.UserReader, interfaces.UserSaver
):
    pass
