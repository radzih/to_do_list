from src.core.application.shared import interfaces


class DBGateway(
    interfaces.Commiter,
    interfaces.TaskReader,
    interfaces.TaskSaver,
    interfaces.TaskRemover,
):
    pass
