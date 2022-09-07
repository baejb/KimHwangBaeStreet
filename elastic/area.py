import pandas as pd
import geopandas as gpd

seoul_area = gpd.GeoDataFrame.from_file('area/TBGIS_TRDAR_RELM.shp', encoding='utf-8')
print(seoul_area.crs)
seoul_area = seoul_area.to_crs(epsg = 4326)
# print(seoul_area)
# seoul_area.to_csv("상권-polygon.csv", encoding='utf-8')
seoul_area.to_file("polygon2.geojson", driver='GeoJSON', encodings='utf-8')