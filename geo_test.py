import json
import geojson
import shapely.geometry
import shapely.ops
from area import area
from shapely.ops import cascaded_union
from functools import reduce


def read_geojson(polygons_file, region_file):
    # reading into two geojson objects
    with open(polygons_file) as geojson1:
        poly1_geojson = json.load(geojson1)
    with open(region_file) as geojson2:
        poly2_geojson = json.load(geojson2)
    return poly1_geojson, poly2_geojson


def get_intersection_area(sentinel_polygon, region):
    # merging the polygons - they are feature collections, containing a point, a polyline, and a polygon - I extract the polygon
    # for my purposes, they overlap, so merging produces a single polygon rather than a list of polygons
    intersection_polygon = sentinel_polygon.intersection(region)
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


def check_cross_polygon(polygons_dict, region):
    intersection_polygons = []
    poly_region = shapely.geometry.asShape(region['features'][0]['geometry'])
    poly_region_default_area = area(
        geojson.Feature(geometry=poly_region, properties={}).geometry)
    for main_el in polygons_dict['features']:
        for child_el in polygons_dict['features']:
            main_poly = shapely.geometry.asShape(main_el['geometry'])
            # print(main_poly)
            child_poly = shapely.geometry.asShape(child_el['geometry'])
            intersection_polygon = main_poly.intersection(child_poly)
            control_area = area(
                geojson.Feature(geometry=child_poly, properties={}).geometry)
            if not intersection_polygon.is_empty and area(
                    geojson.Feature(geometry=intersection_polygon, properties={}).geometry) < control_area:
                intersection_region = poly_region.intersection(intersection_polygon)
                intersection_region_area = area(geojson.Feature(geometry=intersection_region, properties={}).geometry)
                if float("{0:.3f}".format(intersection_region_area)) == float(
                        "{0:.3f}".format(poly_region_default_area)):
                    intersection_polygons.append(intersection_region)

    u = cascaded_union(intersection_polygons)
    geojson_out = geojson.Feature(geometry=u, properties={})
    print(geojson_out)


def iterator(sentinel_polygons, region):
    poly_region = shapely.geometry.asShape(region['features'][0]['geometry'])
    iteration_range = len(sentinel_polygons['features'])
    polygon_idx = 0
    while polygon_idx < iteration_range:
        poly_sentinel = shapely.geometry.asShape(sentinel_polygons['features'][polygon_idx]['geometry'])
        suitable_region = get_intersection_area(poly_sentinel, poly_region)
        if not suitable_region:
            del sentinel_polygons['features'][polygon_idx]
            iteration_range -= 1
        else:
            del sentinel_polygons['features'][polygon_idx]['properties']["description"]
            polygon_idx += 1
    return sentinel_polygons


def main():
    [sentinel_polygons, region] = read_geojson("sentinel2_tiles.geojson", "kharkiv_region.geojson")
    suitable_regions = iterator(sentinel_polygons, region)
    cross_polygon = check_cross_polygon(suitable_regions, region)
    # print(suitable_regions)


if __name__ == '__main__':
    main()
