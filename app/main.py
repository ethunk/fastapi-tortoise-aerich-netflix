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


def raise_exception(detail='An error occured'):
    raise HTTPException(status_code=400, detail=detail)


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
    order_by: Optional[str] = Query(None, description='Accepts a model attribute. Prefix with `-` for descending.'),
):
    content = Content.all()

    if type is not None and type.upper() in ContentType._member_names_:
        content = content.filter(type=type.capitalize())
    elif type is not None:
        raise_exception(detail=f'{type} is not a valid option for `type`.')

    if rating is not None and _snake_case(rating).upper() in Rating._member_names_:
        content = content.filter(rating=rating.upper())
    elif rating is not None:
        raise_exception(detail=f'{rating} is not a valid option for `rating`.')

    if order_by in ContentOutGet.schema()['properties'].keys():
        content.order_by(order_by)
    elif order_by is not None:
        raise_exception(detail=f'{order_by} is not an attribute that can be ordered by.')

    return paginate(await ContentOutGet.from_queryset(content), params)


@app.get('/content/{id}', response_model=ContentOutGet)
async def get_content_by_id(id: str):
    return await ContentOutGet.from_queryset_single((Content.get(id=id)))


# POST/CREATE
@app.post('/content', response_model=ContentOutPost)
async def create_content(content: ContentIn):
    new_content = await Content.create(**content.dict())

    return new_content


# PATCH/UPDATE
@app.patch('/content/{id}', response_model=ContentOutGet)
async def update_content(new_content: ContentIn, id: str):
    old_content = await Content.get(id=id)
    old_content.update_from_dict(new_content.dict())

    return old_content
