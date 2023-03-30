from flask import Blueprint

index_bp = Blueprint('index', __name__)
user_bp = Blueprint('user', __name__)

from app.routes import index, user
