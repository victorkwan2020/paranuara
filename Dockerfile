FROM python:3.8.3-slim-buster

WORKDIR /root/
COPY . /root/

RUN pip install -r requirements.txt \
    && python -m unittest -vvv test.test_app

CMD ["python","-m", "paranuara.app"]
