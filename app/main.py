import logging
from typing import Optional

from app.db import init_db
from app.models import (
    Content, ContentIn, ContentOutGet, ContentOutPost, ContentType, Rating
)
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi_pagination import Page
from fastapi_pagination.paginator import paginate
from fastapi_pagination.params import PaginationParams
from starlette.responses import RedirectResponse

log = logging.getLogger(__name__)

def _snake_case(slug: str):
    return slug.replace('-', '_')

def create_application():
    application = FastAPI()
    return application

app = create_application()

@app.on_event('startup')
async def startup_event():
    print('Starting up...')
    init_db(app)


@app.on_event('shutdown')
async def shutdown_event():
    print('Shutting down...')

@app.get('/')
def redirect_to_docs():
    return RedirectResponse('/docs#')

# GET
@app.get('/content', response_model=Page[ContentOutGet])
async def get_content(
    params: PaginationParams = Depends(),
    type: Optional[str] = Query(None, description="Either ``'Movie'`` or ``'Show'``."),
    rating: Optional[str] = Query(None, description="Valid MPAA or TV Parental Guidelines Monitoring Board rating."),
):
    content = Content.all()
    if type is not None and type.upper() in ContentType._member_names_:
        content = content.filter(type=type.capitalize())
    elif type is not None:
        raise HTTPException(status_code=400, detail=f'{type} is not a valid option for `type`.')

    if rating is not None and _snake_case(rating).upper() in Rating._member_names_:
        content = content.filter(rating=rating.upper())
    elif rating is not None:
        raise HTTPException(status_code=400, detail=f'{rating} is not a valid option for `rating`.')

    return  paginate(await ContentOutGet.from_queryset(content), params)

@app.get('/content/{id}', response_model=ContentOutGet)
async def get_content_by_id(id: str):
    return await ContentOutGet.from_queryset_single((Content.get(id=id)))

# POST/CREATE
@app.post('/content', response_model=ContentOutPost)
async def update_show(show: ContentIn):
    show = await Content.create(**show.dict())

    return show


# PATCH/UPDATE
@app.patch('/content/{id}', response_model=ContentOutGet)
async def update_show(new_content: ContentIn, id: str):
    old_content = await Content.get(id=id)
    old_content.update_from_dict(new_content.dict())

    return old_content
