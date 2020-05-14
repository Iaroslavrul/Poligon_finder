import json
import geojson
from functools import partial
import pyproj
import shapely.geometry
import shapely.ops
from area import area

# checking to make sure they registered as polygons


# merging the polygons - they are feature collections, containing a point, a polyline, and a polygon - I extract the polygon
# for my purposes, they overlap, so merging produces a single polygon rather than a list of polygons
# mergedPolygon = poly1.intersection(poly2)

# using geojson module to convert from WKT back into GeoJSON format
geojson_out = geojson.Feature(geometry=mergedPolygon, properties={})

# outputting the updated geojson file - for mapping/storage in its GCS format
with open('Merged_Polygon.json', 'w') as outfile:
    json.dump(geojson_out.geometry, outfile, indent=3)
outfile.close()

# reprojecting the merged polygon to determine the correct area
# it is a polygon covering much of the US, and dervied form USGS data, so using Albers Equal Area
# project = partial(
#     pyproj.transform,
#     pyproj.Proj(init='epsg:4326'),
#     pyproj.Proj(init='epsg:5070'))
#
# mergedPolygon_proj = shapely.ops.transform(project, mergedPolygon)

with open('Merged_Polygon.json') as geojson3:
    poly3_geojson = json.load(geojson3)
obj = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            35.4638671875,
                            50.43651601698633
                        ],
                        [
                            34.661865234375,
                            50.0289165635219
                        ],
                        [
                            34.78271484375,
                            48.95497369808868
                        ],
                        [
                            36.37573242187499,
                            48.378145469762444
                        ],
                        [
                            37.41943359375,
                            48.785151998043155
                        ],
                        [
                            38.3038330078125,
                            49.44312875803005
                        ],
                        [
                            37.91931152343749,
                            50.41201824668217
                        ],
                        [
                            36.6009521484375,
                            50.55532498251967
                        ],
                        [
                            35.4638671875,
                            50.43651601698633
                        ]
                    ]
                ]
            }
        }
    ]
}
print(area(poly3_geojson))
print(area(obj['features'][0]['geometry']))


def read_geojson(poligons_file, region_file):
    # reading into two geojson objects, in a GCS
    with open('big_area.json') as geojson1:
        poly1_geojson = json.load(geojson1)
    poly1 = shapely.geometry.asShape(poly1_geojson['features'][0]['geometry'])
    with open('little_area.json') as geojson2:
        poly2_geojson = json.load(geojson2)
    # pulling out the polygons
    poly2 = shapely.geometry.asShape(poly2_geojson['features'][0]['geometry'])
    print(poly1.geom_type)
    print(poly2.geom_type)
    return poly1, poly2


def iterator(sentinel_poligons, region):
    return


def main():
    [poligons, region] = read_geojson("sentinel2_tiles.geojson", "Kharkiv_region.geojson")


if __name__ == '__main__':
    main()
