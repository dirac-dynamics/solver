# Usage

No Jupyter notebooks!
~~The Jupyter notebooks are intended to speed up prototyping. In order to have a consistent environment across all devs of `Dirac Dynamics`, please run jupyter through the provided Dockerfile.~~

Happy coding! :-)

## Prerequisites

* Docker

## Run Scripts

To have synchronized environments, please put all your `.python` scrpits in the `/src` folder and run them only inside the Docker container, following the steps:

### Build Container

This step is necessary the first time you start working _and_ every time you make changes on the `requirements.txt`!

```
docker build -t diracdynamics/solver .
```

### Run Container

When you have built the latest version of the container, execute it with the following command:

- On Mac, Linux, Windows Powershell:

```
docker run -it -v ${PWD}/src:/src diracdynamics/solver /bin/bash
```

- On Windows no Powershell:

```
docker run -it -v %cd%/src:/src diracdynamics/solver /bin/bash
```

This will start a docker container with all necessary pip requirements installed (check to build the Docker container after changing the `requiments.txt`!). You can edit any file inside your favourite IDE in the `/src` folder of this repository and execute them _inside_ the running docker container with `python {YOUR_SCRIPT_NAME}.py`. 

## Troubleshooting

- If you are using Mac and have problems accessing the notebooks in the browser, pleaske make sure you have [Desktop for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac/) installed. [This](https://forums.docker.com/t/port-forward-not-working-on-a-macos-installation-but-works-on-others/77401/6) might be your issue.
