FROM python:3.12.3-slim as base
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Development stage:
FROM base as development

CMD ["flask", "run", "--host=0.0.0.0"]

# testing stage:
FROM base as test

CMD ["pytest", "--maxfail=1", "--disable-warnings", "-v"]
