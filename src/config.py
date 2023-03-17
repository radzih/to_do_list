from dataclasses import dataclass

from src.infrastructure.database.config import Database
from src.infrastructure.database.config import load_config as load_db_config


@dataclass
class Config:
    db: Database


def load_config() -> Config:
    return Config(db=load_db_config())
