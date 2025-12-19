from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.core.templates import templates

router = APIRouter(tags=['web'])

@router.get('/', response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse('start_dashboard.html',
                                      {'request': request}
                                      )