FROM python:3.8-slim

# Install System utils req. for gcc, GDAL, GEOS packages...

RUN apt-get update &&\
    apt-get install -y \
        wget \ 
        unzip \
        build-essential \
        proj-bin \
        libproj-dev \
        proj-data \
        proj-bin \
        gdal-bin \
        libgdal-dev \
        libgeos-dev \
        jupyter-notebook &&\
    apt-get clean

# Install GDAL - Required for Shapley; 
# NOTE: 
#   - The Shapely GEOS version (3.8.0-CAPI-1.13.1 ) and GEOS version PyGEOS was 
#     compiled with (3.9.0-CAPI-1.16.2) are compatible, but will warn user 
RUN wget https://github.com/OSGeo/gdal/releases/download/v3.2.1/gdal-3.2.1.tar.gz &&\ 
    gunzip gdal-3.2.1.tar.gz 

# Install GEOS - Required for CartoPy
RUN wget http://download.osgeo.org/geos/geos-3.9.1.tar.bz2 &&\
    bzip2 -d geos-3.9.1.tar.bz2

# Python Installs, split by general category of import:
#   - Install Geospatial Support Libraries + JupyterHub minimal reqs, 
#   many redundant installs, left in for clarity. 
#
#   - No cache for Img Size Control: 
#       - https://pip.pypa.io/en/stable/reference/pip_install/#caching
#
#   - See Note on Shapely building from binary: https://pypi.org/project/Shapely/

# General Numeric Stack
RUN pip install --upgrade pip &&\
        pip install --no-cache-dir \
        Cython \
        pandas \
        numpy \
        scipy \
        sklearn

# Common Plotting        
RUN pip install --no-cache-dir \
        matplotlib \
        seaborn

# Common Mapping - From GeoPandas Docs
RUN pip install --no-cache-dir \
        geopandas \
        mapbox \
        descartes \
        contextily \
        pygeos \
        geoplot \
        shapely \ 
        mapclassify \
        folium \
        libpysal \
        --no-binary shapely

# Jupyter Installs + Misc
RUN pip install --no-cache-dir \
        notebook>=5.0 \
        psycopg2-binary
        
# Create a user to avoid running container as root, using `diver`
RUN useradd -m diver

ENV HOME=/home/diver/

WORKDIR $HOME

USER diver

# Start SingleUser JupyterHub NB Cluster on Container Init...
CMD ["jupyter-notebook",  "--ip=0.0.0.0"]

