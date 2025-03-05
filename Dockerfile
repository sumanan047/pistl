FROM python:3.12

WORKDIR /pistl

RUN pip install poetry
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-root

COPY . .
RUN poetry install --no-root

RUN python --version

#ENTRYPOINT ["top", "-b"]

# TODO: run the test suite and check if the dockerization is correct.
# TODO: Currently, one of the test cases if failing
RUN pytest -v -rA