import json
import unittest
from geo_test import iterator, remove_excess_polygon, check_cross_polygon, get_intersection_area


class Sentinel2overlapTest(unittest.TestCase):
    def test_suitable_regions(self):
        with open('sentinel2_tiles.geojson') as geojson1:
            poly1_geojson = json.load(geojson1)
        with open('kharkiv_region.geojson') as geojson2:
            poly2_geojson = json.load(geojson2)
        with open('suitable_regions_test_valid.geojson') as geojson_res:
            expected_response = json.load(geojson_res)
        test_request = iterator(poly1_geojson, poly2_geojson)
        self.assertEqual(test_request, expected_response)

    def test_remove_excess_polygon(self):
        with open('sentinel2_tiles.geojson') as geojson1:
            poly1_geojson = json.load(geojson1)
        with open('excess_test.geojson') as geojson2:
            poly2_geojson = json.load(geojson2)
        with open('remove_excess_polygon_valid.geojson') as geojson_res:
            expected_response = json.load(geojson_res)
        test_request = remove_excess_polygon(poly1_geojson, poly2_geojson)
        self.assertEqual(test_request, expected_response)

    def test_check_cross_polygon(self):
        with open('sentinel2_tiles.geojson') as geojson1:
            poly1_geojson = json.load(geojson1)
        with open('cross_test.geojson') as geojson2:
            poly2_geojson = json.load(geojson2)
        with open('cross_test_valid.geojson') as geojson_res:
            expected_response = json.load(geojson_res)
        test_request = remove_excess_polygon(poly1_geojson, poly2_geojson)
        self.assertEqual(test_request, expected_response)

    def test_get_intersection_area(self):
        with open('sentinel2_tiles.geojson') as geojson1:
            poly1_geojson = json.load(geojson1)
        with open('cross_test.geojson') as geojson2:
            poly2_geojson = json.load(geojson2)
        with open('cross_test_valid.geojson') as geojson_res:
            expected_response = json.load(geojson_res)
        test_request = remove_excess_polygon(poly1_geojson, poly2_geojson)
        self.assertEqual(test_request, expected_response)


unittest.main()
