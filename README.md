# FastAPI + Tortoise-ORM + Aerich

## To run locally
You will need to set the environment variable for `DATABASE_URL` either in a .env file or explicitly in the Dockerfile

Then there are the following options to run locally.

- Option 1:
  - Docker build image locally and run

- Option 2:
  - Create a python virtual environment (.tool-versions specifies python 3.7.1, recommend using asdf)
  - `pip install -r ./requirements.txt`
  - Setup the database (optional, can be handled by tortoise ORM if starting from scratch)
```
aerich init -t app.db.TORTOISE_ORM
aerich init-db
aerich migrate
aerich upgrade
```
  - You can pip install pandas and ipython. Then start an ipython session and copy and paste the code from the `create_data_records.py` file to populate your database
  - run `uvicorn app.main:app --reload`
  - visit: `localhost:8000/` or `127.0.0.1:8000/`


Running Test:
`pytest`
```
╰➜ pytest
============================================================ test session starts ============================================================
platform darwin -- Python 3.7.1, pytest-6.2.1, py-1.10.0, pluggy-0.13.1
rootdir: /Users/erichunkler/Documents/projects/fastapi-tortoise-aerich-netflix
plugins: asyncio-0.14.0
collected 3 items

app/test_api.py ...                                                                                                                   [100%]

============================================================= 3 passed in 2.52s =============================================================
```
