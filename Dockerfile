FROM gboeing/osmnx

COPY requirements.txt /tmp/

# configure conda and install packages in one RUN to keep image tidy
RUN pip install -r /tmp/requirements.txt

RUN mkdir src
WORKDIR /src/

CMD ["jupyter", "lab", "--ip='0.0.0.0'", "--port=8888", "--no-browser", "--NotebookApp.token=''", "--NotebookApp.password=''"]

