import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from geopandas import GeoSeries

map = gpd.read_file("Longitude_Graticules_and_World_Countries_Boundaries-shp/99bfd9e7-bb42-4728-87b5-07f8c8ac631c2020328-1-1vef4ev.lu5nk.shp") # import world map
# crs = {"init":"espc:4326"} # designate coordinate system
map.to_crs(epsg=4326)

df = pd.read_csv("combined.csv")
df = df[df["label"] == "on-topic"]
df['frequency'] = df.groupby('latitude')['longitude'].transform('size')
df.drop_duplicates(subset =["latitude"], inplace = True)

# merge shapefile with data
merge = map.merge(df, left_on = "CNTRY_NAME", right_on = "country")

mymap = folium.Map(zoom_start=10)
folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(mymap)

colors = {
    "bombing": "#f6c7b0",
    "explosion": "#f4f390",
    "flood": "#f5c864",
    "hurricane": "#b3e8fs",
    "tornado": "ae8cf4"
}

for i, j in merge.iterrows():
    long = merge.iloc[[i]]["longitude"].item()
    lat = merge.iloc[[i]]["latitude"].item()
    cat = merge.iloc[[i]]["category"].item()
    freq = merge.iloc[[i]]["frequency"].item()
    folium.CircleMarker(
        location=[lat, long],
        radius=10,
        popup=[cat, freq],
        color=colors.get(cat),
        fill=True,
        fill_color=colors.get(cat),
    ).add_to(mymap)

folium.LayerControl().add_to(mymap)

mymap.save("index.html")
