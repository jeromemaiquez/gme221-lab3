# GmE 221 - Laboratory Exercise 1

## Overview
This laboratory exercise constructs true 3D `LineString` geometries whose coordinates include a Z value (derived from a DEM raster). PostGIS is used for geospatial data storage.

## Environment Setup
- Python 3.x
- PostgreSQL with PostGIS
- GeoPandas, SQLAlchemy, psycopg2, rasterio, Flask

## How to Run
1. Activate the virtual environment
2. Run `analysis.py` to derive Z values in road vertices from DEM raster

## Outputs
- Shapefile of 3D `LineString` geometries
- GeoJSON of 3D `LineString` geometries