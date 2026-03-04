import geopandas as gpd
from sqlalchemy import create_engine

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

print(roads.head())
print(roads.crs)
print(roads.geometry.type.unique())