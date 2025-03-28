from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importa os models para que o SQLAlchemy os conheça
from api.models.user_model import User