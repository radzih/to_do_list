from src.infrastructure.database import repositories


class DBGateway(
    repositories.Commiter,
    repositories.TaskReader,
    repositories.TaskSaver,
    repositories.TaskRemover,
    repositories.UserReader,
    repositories.UserSaver,
):
    pass
