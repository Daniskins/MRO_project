from starlette.templating import Jinja2Templates

from app.core.paths import TEMPLATES_DIR

templates = Jinja2Templates(directory=TEMPLATES_DIR)