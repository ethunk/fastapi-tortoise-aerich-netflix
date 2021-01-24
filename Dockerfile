# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.7-slim-buster

ENV DATABASE_URL=postgres://eric:@localhost:5432/netflix

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL=postgres://postgres:Mx6IEl6LzJ32kwe2@104.196.29.24:5432/netflix2
# Environment Variables

# Install pip requirements
RUN pip install --upgrade pip
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN useradd appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
EXPOSE 8000 80

CMD ["uvicorn", "app.main:app", "--reload"]
