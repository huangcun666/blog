from flask import Blueprint
from config import Config

main = Blueprint('main', __name__,static_folder=Config.PROJECT_PATH+'/app/static')

from . import views, errors
from ..models import Permission


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
