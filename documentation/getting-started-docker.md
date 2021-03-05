# Getting Started With Docker

This docuement discusses how to install Docker and start a container with a suite of common geospatial analysis and visualization packages pre-installed, including [GeoPandas](https://geopandas.org/gallery/index.html), [Cartopy](https://scitools.org.uk/cartopy/docs/latest/gallery/index.html), and [Folium](https://geopandas.org/gallery/polygon_plotting_with_folium.html) Also consider reading through a primer on [GIS](https://mgimond.github.io/Spatial/introGIS.html), map-making, etc. (code examples in R, but the logic is generalized to all GIS work)

Following the steps below should allow you to explore and visualize data for these counties in an isolated, stable environment without trying to resolve dependancies and installation on your machine.

------

## Docker Installation

If you've already got Docker Desktop installed on your machine you can skip this section. Otherwise, follow the [install guide](https://docs.docker.com/get-docker) from the Docker documentation. If you aren't familiar with Docker you can refer to this [section](https://docs.docker.com/get-started/#what-is-a-container) of the docs and the embeded video to learn more.

------

## Building the Image

Once Docker Desktop is installed, run the following from the root of the `housing-insecurity` repo to build and "tag" (name) your image. This step may take a few minutes.

```bash
docker build ./docker/Jupyter/ \
    -t flh-quickstart-jupyter
```

The `docker build` command runs the installation and configuration steps defined in `./docker/Jupyter/Dockerfile` to on top of a new Python 3.8 installation. Once an image is created, you can quickly start, stop, and launch multiple containers using the image as a template.

------

## Running the Container

To start a container, run the following command from the root of the `housing-insecurity` repo.

```bash
docker run -p 8888:8888 \
    --name flh-geoviz \
    -v $(pwd):/home/diver/datadive flh-quickstart-jupyter
```

The `-p` flag maps the port that Juyter is running on in the container (`8888`) to your machine's port `8888`. This allows you to access the container from `https://127.0.0.1:8888` in any browser as if you were running a notebook server on your machine.

The `-v` flag creates a volume. Volumes allows you to access project materials from your machine in docker container and persist content from the container to your host machine.

If everything has gone properly, you should see an output similar to the following in your terminal.

```bash
[I 05:15:10.468 NotebookApp] http://127.0.0.1:8888/?token=<TOKEN>
```

Copy that line into a browser, replacing the token with what appears in your terminal. A notebook server should appear. Navigate to `./examples/getting_started.ipynb` to confirm your environment is working properly and take a look at some of the example maps.

------

## Maintaining and Updating your environment

You may pip install additional packages in this container by launching a terminal from `https://127.0.0.1:8888/tree`. See [screenshot](https://tljh.jupyter.org/en/latest/_images/new-terminal-button3.png).
