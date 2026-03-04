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

## Reflections: Part C

1. As a spatial RDBMS, PostGIS has many features that make it highly suitable for storing (and analyzing) vector layers (e.g., road network). Down the line, if the project were to need more vector layers (e.g., parcels, land use), PostGIS can serve as a single source of truth AND a powerful analytical engine, all in one place.
2. Meanwhile, rasters are often too large to be stored and analyzed efficiently in PostGIS, which is better suited for handling tabular data (e.g., vector layers). As such, the DEM was instead imported into Python from a TIF file.
3. Hybrid I/O strategies are used in real-world GIS architecture to account for the differences between vector and raster data. Even cutting-edge formats take these differences into account: cloud-native vector formats such as GeoParquet are created for faster handling in DBMSs such as DuckDB, while cloud-native raster formats such as Cloud Optimized GeoTIFFs are still made to be accessed tile-wise from a data lake.
4. No spatial analysis is yet occurring at this stage. So far, we have only ingested the roads and DEM datasets from their respective storage models into the unified environment of Python.