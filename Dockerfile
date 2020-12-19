FROM gboeing/osmnx

COPY requirements.txt /tmp/

# configure conda and install packages in one RUN to keep image tidy
RUN pip install -r /tmp/requirements.txt

RUN mkdir src
WORKDIR /src/

ENTRYPOINT ["/bin/sh", "-c"]

