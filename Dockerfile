FROM python:3.13-slim

RUN pip install \
    asyncua==1.0.2

WORKDIR /opt/opc_mockup/datagenerator

COPY ./src /opt/opc_mockup/datagenerator

CMD [ "python" ,"./server-minimal.py"]