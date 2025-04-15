import plotly.express as px
import pandas as pd
import json

with open("./compiled/combined_postcode_price_coords.json") as f:
    data = json.load(f)

df = pd.DataFrame(data)

fig = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    hover_name="postcode",
    hover_data={"price": True},
    color="price",
    color_continuous_scale="Viridis",
    range_color=(100000, 800000),  # or whatever range makes sense
    zoom=5,
    height=900
)

fig.update_layout(mapbox_style="carto-positron")
fig.write_html("uk_property_map.html")
