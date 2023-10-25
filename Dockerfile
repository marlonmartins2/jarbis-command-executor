FROM python:3.10

ENV PYTHONPATH="${PYTHONPATH}:/"

ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /app

COPY ./app/. .version ./ requirements.txt ./

RUN pip install -q --upgrade pip

RUN pip install -q --no-cache-dir --upgrade -r requirements.txt

RUN python -m spacy download pt_core_news_sm

EXPOSE 80

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80", "--use-colors"]
