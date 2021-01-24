import os
import pandas as pd

from app.models import Content, ContentType, Rating
from datetime import datetime
from tortoise.exceptions import IntegrityError
from tortoise import Tortoise

DATE_FORMAT = '%d-%b-%y'

async def init():
     # Here we connect to a DATABASE_URL file.
     # also specify the app name of "models"
     # which contain models from "app.models"
     await Tortoise.init(
         db_url=os.environ.get("DATABASE_URL"),
         modules={'models': ['app.models']}
     )
     # Generate the schema
     await Tortoise.generate_schemas()

await init()

df = pd.read_csv('netflix_titles.csv')
records = df.to_records(index=False)

new_items_list = []
for record in records:
    id_, type_, title, date_added, release_year, rating, duration, description = record
    try:
        new_item = Content(
            # id=id_,
            type=ContentType._value2member_map_.get(type_),
            title=title,
            date_added=datetime.strptime(date_added, DATE_FORMAT) if date_added == date_added else None,
            rating=Rating._value2member_map_.get(rating),
            duration=int(duration.strip('minseason')) if duration else None,
            description=description,
            release_year=release_year if release_year else None,
        )
        new_items_list.append(new_item)
    except (ValueError, IntegrityError):
        continue

await Content.bulk_create(new_items_list)

await Tortoise.close_connections()
