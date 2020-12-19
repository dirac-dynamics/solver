# Usage

The Jupyter notebooks are intended to speed up prototyping. In order to have a consistent environment across all devs of `Dirac Dynamics`, please run jupyter through the provided Dockerfile.

Happy coding! :-)

## Prerequisites

* Docker

## Run Jupyter

In order to work on the notebook, please build & run the docker container with the following commands.

### Build Container

This step is necessary the first time you start working _and_ every time you make changes on the `requirements.txt`!

```
docker build -t diracdynamics/prototyping .
```

### Run Container

When you have built the latest version of the container, execute it with the following command:

- On Mac, Linux, Windows Powershell:

```
docker run -p 8888:8888 -v ${PWD}/notebooks:/src/notebooks diracdynamics/prototyping
```

- On Windows no Powershell:

```
docker run -p 8888:8888 -v %cd%/notebooks:/src/notebooks diracdynamics/prototyping
```

This will start a docker container running the Jupyter notebook. The address of the server will be shown in the cli.

## Troubleshooting

- If you are using Mac and have problems accessing the notebooks in the browser, pleaske make sure you have [Desktop for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac/) installed. [This](https://forums.docker.com/t/port-forward-not-working-on-a-macos-installation-but-works-on-others/77401/6) might be your issue.