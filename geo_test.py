import json
import sys

import geojson
import shapely.geometry
import shapely.ops
from area import area
import copy
from shapely.ops import cascaded_union

# input_file_path = sys.argv[1]
# output_file_path = sys.argv[2]

input_file_path = 'kharkiv_region.geojson'
output_file_path = 'Merged_Polygon.json'


def read_geojson(polygons_file, region_file):
    # Чтение двух объектов Geojson
    with open(polygons_file) as geojson1:
        poly1_geojson = json.load(geojson1)
    with open(region_file) as geojson2:
        poly2_geojson = json.load(geojson2)
    return poly1_geojson, poly2_geojson


def get_intersection_area(sentinel_polygon, region):
    # Нажождения общего вхождения многоугольников - это наборы объектов, содержащие точку, ломаную линию и многоугольник - я извлекаю многоугольник
    # для моих целей они перекрываются, поэтому при слиянии получается один полигон, а не список полигонов
    intersection_polygon = sentinel_polygon.intersection(region)
    if not intersection_polygon.is_empty and area(
            geojson.Feature(geometry=intersection_polygon, properties={}).geometry) > 1000:
        return area(geojson.Feature(geometry=intersection_polygon, properties={}).geometry)
    else:
        pass


def check_cross_polygon(polygons_dict, region):
    result_poly_name = ''
    start_len = len(polygons_dict['features'])
    poly_names = []
    poly_region = shapely.geometry.asShape(region['features'][0]['geometry'])
    poly_region_default_area = area(
        geojson.Feature(geometry=poly_region, properties={}).geometry)
    for main_el in polygons_dict['features']:
        for child_el in polygons_dict['features']:
            intersection_region_area = 0
            main_poly = shapely.geometry.asShape(main_el['geometry'])
            child_poly = shapely.geometry.asShape(child_el['geometry'])
            intersection_polygon = main_poly.intersection(child_poly)
            control_area = area(
                geojson.Feature(geometry=child_poly, properties={}).geometry)
            if not intersection_polygon.is_empty and area(
                    geojson.Feature(geometry=intersection_polygon, properties={}).geometry) < control_area:
                intersection_region = poly_region.intersection(intersection_polygon)
                if not intersection_region.is_empty:
                    intersection_region_area = area(
                        geojson.Feature(geometry=intersection_region, properties={}).geometry)
                if float("{0:.2f}".format(intersection_region_area)) == float(
                        "{0:.2f}".format(poly_region_default_area)):
                    poly_names.append(main_el["properties"]["Name"])
                    poly_names.append(child_el["properties"]["Name"])
    if poly_names:
        result_poly_name = sorted(set(poly_names))[0]
        for inter_poly in range(len(polygons_dict['features'])):
            if polygons_dict['features'][inter_poly]["properties"]["Name"] != result_poly_name:
                del polygons_dict['features'][inter_poly]
    if len(polygons_dict['features']) != start_len:
        return polygons_dict
    else:
        return None


def remove_excess_polygon(polygons_dict, region):
    start_len = len(polygons_dict['features'])
    poly_region = shapely.geometry.asShape(region['features'][0]['geometry'])
    poly_region_default_area = area(
        geojson.Feature(geometry=poly_region, properties={}).geometry)
    idx = 0
    iteration_range = len(polygons_dict['features'])
    while idx < iteration_range:
        intersection_polygon_area = 0
        poly_list = []
        poly_copy = copy.deepcopy(polygons_dict)
        del poly_copy['features'][idx]
        for el in poly_copy['features']:
            el_poly = shapely.geometry.asShape(el['geometry'])
            poly_list.append(el_poly)
        union_poly = cascaded_union(poly_list)
        intersection_polygon = union_poly.intersection(poly_region)
        if not (intersection_polygon.is_empty and union_poly.is_empty):
            intersection_polygon_area = area(geojson.Feature(geometry=intersection_polygon, properties={}).geometry)
        else:
            break
        if float("{0:.2f}".format(poly_region_default_area)) == float("{0:.2f}".format(intersection_polygon_area)):
            del polygons_dict['features'][idx]
            iteration_range -= 1
        else:
            idx += 1
    if len(polygons_dict['features']) > 0 and (len(polygons_dict['features']) != start_len):
        return polygons_dict
    else:
        return None


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


def result_writer(result_poly):
    # Запись найденной коллекции геометрий в файл в формате geojson
    with open(output_file_path, 'w') as outfile:
        json.dump(result_poly, outfile, indent=3)
    outfile.close()


def choice_to_write(suitable_regions, cross_polygon, excess_poly):
    if cross_polygon:
        print('cross_polygon')
        return cross_polygon
    if excess_poly:
        print('excess_poly')
        return excess_poly
    else:
        print("suitable_regions")
    return suitable_regions


def main():
    [sentinel_polygons, region] = read_geojson("sentinel2_tiles.geojson", input_file_path)
    suitable_regions = iterator(sentinel_polygons, region)
    excess = remove_excess_polygon(copy.deepcopy(suitable_regions), region)
    cross_polygon = check_cross_polygon(copy.deepcopy(suitable_regions), region)
    result_choice = choice_to_write(suitable_regions, cross_polygon, excess)
    # print(excess)
    # print(cross_polygon)
    # print(sentinel_polygons)
    print(result_choice)
    # result_writer(excess)


if __name__ == '__main__':
    main()
