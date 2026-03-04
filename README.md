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

## Reflections: Part D
1. The original LineString objects only had few vertices each, typically the endpoints plus points of bending or intersection with other LineString objects. This is too sparse to capture fine gradations in the elevation, preventing the roads to be modeled fully as 3D objects. As such, densification was necessary to allow a finer sampling of the elevation along the roads.
2. CRS alignment is necessary before sampling to ensure that the road sample vertices and DEM lie on the same coordinate system. Since sampling relies on a co-location, the sample vertex and its corresponding raster pixel must be located in the same location in the same CRS.
3. Since the geometries now have a proper Z dimension, their elevation can now be modeled as a dimension of its location (in addition to latitude and longitude). This allows true 3D representation and analysis. For example, the length of the road segments will now change to account for any elevation change.

## Final Reflections
1. Export to GeoJSON preserves the 3-dimensional coordinate structure of the LineString objects (each vertex is defined by an (x, y, z) tuple).
2. GeoJSON lacks a specific `LineStringZ` geometry type to denote 3D LineString objects. Instead, the geometries are of type `LineString`.
3. This is because GeoJSON simply lacks the `LineStringZ` geometry type in its specification (data standard), despite nonetheless being able to support a 3D coordinate structure (in content).
4. Given the 3D coordinate structure, QGIS is able to handle and visualize the road features as true 3D geometry. This is in contrast to 2.5D visualizations, where a nonetheless 2D layer (viewed top-down) is given the illusion of height/depth using a height/elevation attribute.
5. Other geospatial vector file/storage formats with more explicit 3D support include GeoPackage, CityGML, or storage in PostGIS. In these formats, 3D-specific geometry types are available (e.g., `LineStringZ`), which can undergo 3D operations.