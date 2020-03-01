FROM python:3.8-buster

WORKDIR /usr/src/app
ENV PYTHONPATH=/usr/src/app

COPY poetry.lock pyproject.toml ./
RUN pip install --no-cache-dir -U pip wheel setuptools \
 && pip install --no-cache-dir poetry \
 && poetry config virtualenvs.create false \
 && poetry install --no-dev

COPY compose/app/start.sh /start.sh
RUN chmod +x /start.sh

COPY . .

EXPOSE 8080

CMD ["/start.sh"]
