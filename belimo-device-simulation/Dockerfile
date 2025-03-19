ARG BASE_IMAGE=python:3.9-slim
FROM $BASE_IMAGE

USER 0

COPY . /belimo-cloudsimulation
WORKDIR /belimo-cloudsimulation

RUN pip3 install --no-cache-dir -r requirements.txt \
    && pip3 install .

CMD ["/bin/bash"]
