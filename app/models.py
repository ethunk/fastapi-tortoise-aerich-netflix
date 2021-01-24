import datetime

from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from enum import Enum

"""
Tortoise models.
"""

class ContentType(str, Enum):
    SHOW = "Show"
    MOVIE = "Movie"

class Rating(str, Enum):
    TV_MA = 'TV-MA'
    TV_G = 'TV-G'
    UR = 'UR'
    TV_14 = 'TV-14'
    TV_PG = 'TV-PG'
    TV_Y7_FV = 'TV-Y7-FV'
    NR = 'NR'
    TV_Y7 = 'TV-Y7'
    R = 'R'
    PG = 'PG'
    TV_Y = 'TV-Y'
    G = 'G'
    PG_13 = 'PG-13'

class Content(Model):
    id = fields.IntField(pk=True, required=False)
    type = fields.CharEnumField(ContentType, description='Either ``"Show"`` or ``"Movie"``', default=ContentType.MOVIE)
    title = fields.CharField(max_length=400, required=False)
    date_added = fields.DateField(auto_now=False, auto_now_add=False, default=datetime.date.today())
    release_year = fields.IntField(null=True)
    rating = fields.CharEnumField(Rating, description="TV or MPAA Rating", default=Rating.NR)
    duration = fields.IntField(required=False)
    description = fields.TextField(null=True)


ContentIn = pydantic_model_creator(Content, name="ContentIn", exclude=('id',))
ContentOutPost = pydantic_model_creator(Content, name="ContentPost", include=('id',))
ContentOutGet = pydantic_model_creator(Content, name="ContentOutGet")
