import osmnx as ox
import matplotlib.pyplot as plt

start_pos = (51.507086,-0.172120)

tags = {
    "amenity": "toilets"
}

DIST = 1500

G = ox.graph_from_point(start_pos, DIST)

gdf_houses = ox.features_from_point(start_pos, { "building": True }, DIST)

gdf_toilets = ox.features_from_point(start_pos, tags, DIST)

fig, ax = ox.plot.plot_figure_ground(G, dist=DIST, default_width=0.1, color='#515151', show=False)

ox.plot.plot_footprints(gdf_houses, ax=ax, figsize=(16, 16), color='#515151', edge_color='orange', edge_linewidth=0, alpha=None, bbox=None, show=False, close=False, save=False, filepath=None, dpi=600)
ox.plot.plot_footprints(gdf_toilets, ax=ax, figsize=(16, 16), color='orange', edge_color='orange', edge_linewidth=0, alpha=None, bbox=None, show=False, close=False, save=False, filepath=None, dpi=600)

plt.show()