import geopandas as gpd
from sqlalchemy import create_engine
import rasterio as rio
from shapely.geometry import LineString, MultiLineString

# --------- DATA INGESTION ----------- #

# Database connection parameters
host = "localhost"
port = "5432"
dbname = "gme221_exer3"
user = "postgres"
password = "postgres"

conn_str = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
engine = create_engine(conn_str)

# Minimal SQL query (no spatial processing)
sql_roads = "SELECT gid, geom FROM public.roads"

roads = gpd.read_postgis(sql_roads, engine, geom_col="geom")

# IMPORTANT: attach CRS (GeoPandas often reads PostGIS geometry without CRS)
roads = roads.set_crs(epsg=3123, allow_override=True)

# print(roads.head())
# print("Roads CRS:", roads.crs)
# print("Roads Geom Type:", roads.geometry.type.unique())

dem = rio.open("data/dem.tif")

# print("DEM CRS:", dem.crs)
# print("DEM Resolution:", dem.res)
# print("DEM Bounds:", dem.bounds)

# ---------- ELEVATION SAMPLING and ----------#
# ---------- LINESTRINGZ CONSTRUCTION ------- #

SAMPLE_STEP = 10    # meters (adjust later for sensitivity)


def densify_line(line: LineString, step: float):
    """Return points sampled along a line at fixed distance spacing."""
    if line.length == 0:
        return []
    
    distances = list(range(0, int(line.length), int(step)))

    pts = [line.interpolate(d) for d in distances]
    pts.append(line.interpolate(line.length))
    
    return pts


def explode_to_lines(geom):
    """Explode MultiLineString features into LineString."""
    match geom.geom_type:
        case "LineString":
            return [geom]
        case "MultiLineString":
            return list(geom.geoms)
        case _:
            return []
        

# Quick test of the sampling function on the first road geometry

# test_geom = roads.geometry.iloc[0]
# lines = explode_to_lines(test_geom)
# pts = densify_line(lines[0], SAMPLE_STEP)
# print("Sample points:", len(pts), "Line length:", lines[0].length)

all_sample_points = []

for geom in roads.geometry:
    parts = explode_to_lines(geom)
    for line in parts:
        pts = densify_line(line, SAMPLE_STEP)
        for pt in pts:
            all_sample_points.append(pt)

gdf_samples = gpd.GeoDataFrame(
    geometry=all_sample_points,
    crs=roads.crs
)

gdf_samples.to_file("output/road_sample_points.shp")
print("Densified sample points exported.")