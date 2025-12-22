from starlette.templating import Jinja2Templates

from app.core.config import settings

templates = Jinja2Templates(directory=settings.paths.templates_dir)