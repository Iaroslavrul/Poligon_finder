import json
import geojson
import shapely.geometry
import shapely.ops
from area import area


def read_geojson(poligons_file, region_file):
    # reading into two geojson objects
    with open(poligons_file) as geojson1:
        poly1_geojson = json.load(geojson1)
    with open(region_file) as geojson2:
        poly2_geojson = json.load(geojson2)
    return poly1_geojson, poly2_geojson


def get_intersection_area(sentinel_poligon, poly_sentinel_name, region):
    # merging the polygons - they are feature collections, containing a point, a polyline, and a polygon - I extract the polygon
    # for my purposes, they overlap, so merging produces a single polygon rather than a list of polygons
    intersection_polygon = sentinel_poligon.intersection(region)
    if intersection_polygon.is_empty:
        pass
    else:
        geojson_out = geojson.Feature(geometry=intersection_polygon, properties={})
        print(area(geojson_out.geometry))

        # outputting the updated geojson file - for mapping/storage in its GCS format
        # with open('Merged_Polygon.json', 'w') as outfile:
        #     json.dump(geojson_out.geometry, outfile, indent=3)
        # outfile.close()
        # with open('Merged_Polygon.json') as geojson3:
        #     poly3_geojson = json.load(geojson3)
        #     print(area(poly3_geojson))
    # using geojson module to convert from WKT back into GeoJSON format

    # outputting the updated geojson file - for mapping/storage in its GCS format
    # with open('Merged_Polygon.json', 'w') as outfile:
    #     json.dump(geojson_out.geometry, outfile, indent=3)
    # outfile.close()


def iterator(sentinel_poligons, region):
    poly_region = shapely.geometry.asShape(region['features'][0]['geometry'])
    for poligon in sentinel_poligons['features']:
        poly_sentinel = shapely.geometry.asShape(poligon['geometry'])
        poly_sentinel_name = poligon['properties']["Name"]
        get_intersection_area(poly_sentinel, poly_sentinel_name, poly_region)

        # print(poly1)


def main():
    [sentinel_poligons, region] = read_geojson("sentinel2_tiles.geojson", "kharkiv_region.geojson")
    iterator(sentinel_poligons, region)


if __name__ == '__main__':
    main()
