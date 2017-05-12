FROM python:2.7.12

RUN apt-get update && apt-get install -y git

RUN pip install scipy numpy --user

WORKDIR /
ADD . /app
WORKDIR /app
RUN pip install -e . --user

ENTRYPOINT ["python", "-m", "cloudbrain.run"]
CMD ["--file", "./examples/source.mock.docker.json"]
