import json
import geojson
import shapely.geometry
import shapely.ops
from area import area
from shapely.ops import cascaded_union
import itertools
from functools import reduce


def read_geojson(poligons_file, region_file):
    # reading into two geojson objects
    with open(poligons_file) as geojson1:
        poly1_geojson = json.load(geojson1)
    with open(region_file) as geojson2:
        poly2_geojson = json.load(geojson2)
    return poly1_geojson, poly2_geojson


def get_intersection_area(sentinel_poligon, region):
    # merging the polygons - they are feature collections, containing a point, a polyline, and a polygon - I extract the polygon
    # for my purposes, they overlap, so merging produces a single polygon rather than a list of polygons
    intersection_polygon = sentinel_poligon.intersection(region)
    if not intersection_polygon.is_empty and area(
            geojson.Feature(geometry=intersection_polygon, properties={}).geometry) > 1000:
        return area(geojson.Feature(geometry=intersection_polygon, properties={}).geometry)
    else:
        pass

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


def check_cross_poligon(poligons_dict, region):
    intersection_poligons = []
    poly_region = shapely.geometry.asShape(region['features'][0]['geometry'])
    for main_el in poligons_dict['features']:
        for child_el in poligons_dict['features']:
            main_poly = shapely.geometry.asShape(main_el['geometry'])
            # print(main_poly)
            child_poly = shapely.geometry.asShape(child_el['geometry'])
            intersection_polygon = main_poly.intersection(child_poly)
            if not intersection_polygon.is_empty and area(
                    geojson.Feature(geometry=intersection_polygon, properties={}).geometry) < 6015317860:
                intersection_poligons.append(intersection_polygon)
    u = cascaded_union(intersection_poligons)
    geojson_out = geojson.Feature(geometry=u, properties={})
    print(geojson_out)


def iterator(sentinel_poligons, region):
    poly_region = shapely.geometry.asShape(region['features'][0]['geometry'])
    iteration_range = len(sentinel_poligons['features'])
    poligon_idx = 0
    while poligon_idx < iteration_range:
        poly_sentinel = shapely.geometry.asShape(sentinel_poligons['features'][poligon_idx]['geometry'])
        suitable_region = get_intersection_area(poly_sentinel, poly_region)
        if not suitable_region:
            del sentinel_poligons['features'][poligon_idx]
            iteration_range -= 1
        else:
            del sentinel_poligons['features'][poligon_idx]['properties']["description"]
            poligon_idx += 1
    return sentinel_poligons


def main():
    [sentinel_poligons, region] = read_geojson("sentinel2_tiles.geojson", "kharkiv_region.geojson")
    suitable_regions = iterator(sentinel_poligons, region)
    cross_poligon = check_cross_poligon(suitable_regions, region)
    # print(suitable_regions)


if __name__ == '__main__':
    main()
