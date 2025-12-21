from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.core.templates import templates

router = APIRouter(prefix='/planes', tags=['planes', 'web'])


@router.get('/new', response_class=HTMLResponse)
async def add_new_aircraft_form(request: Request):
    return templates.TemplateResponse('add_new_aircraft.html',
                                      {'request': request}
                                      )
