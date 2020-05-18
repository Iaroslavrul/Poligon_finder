import json
import unittest

import shapely

from geo_test import iterator, remove_excess_polygon, check_cross_polygon, get_intersection_area


class Sentinel2overlapTest(unittest.TestCase):
    def test_suitable_regions(self):
        with open('sentinel2_tiles.geojson') as geojson1:
            poly1_geojson = json.load(geojson1)
        with open('kharkiv_region.geojson') as geojson2:
            poly2_geojson = json.load(geojson2)
        with open('data_for_tests/suitable_regions_test_valid.geojson') as geojson_res:
            expected_response = json.load(geojson_res)
        test_request = iterator(poly1_geojson, poly2_geojson)
        self.assertEqual(test_request, expected_response)

    def test_remove_excess_polygon(self):
        with open('data_for_tests/cross_test_valid.geojson') as geojson_res:
            poly = json.load(geojson_res)
        with open('data_for_tests/excess_ut_region.geojson') as geojson_reg:
            poly_reg = json.load(geojson_reg)
        test_request = remove_excess_polygon(poly, poly_reg)
        test_request_name = test_request['features'][0]["properties"]["Name"]
        self.assertEqual(test_request_name, "37URQ")

    def test_check_cross_polygon(self):
        with open('data_for_tests/cross_test_valid.geojson') as geojson_res:
            poly = json.load(geojson_res)
        with open('data_for_tests/cross_region_test.geojson') as geojson_reg:
            poly_reg = json.load(geojson_reg)
        test_request = check_cross_polygon(poly, poly_reg)
        test_request_name = test_request['features'][0]["properties"]["Name"]
        self.assertEqual(test_request_name, "37UDQ")

    def test_get_intersection_area(self):
        with open('data_for_tests/get_intersection_area_poly.geojson') as geojson2:
            poly_geojson = json.load(geojson2)
        poly_region = shapely.geometry.asShape(poly_geojson['features'][0]['geometry'])
        poly_sentinel = shapely.geometry.asShape(poly_geojson['features'][1]['geometry'])
        test_request = get_intersection_area(poly_sentinel, poly_region)
        expected_response = 1816896949.2555897
        self.assertEqual(test_request, expected_response)


if __name__ == '__main__':
    unittest.main()
