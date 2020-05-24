import json
import unittest

from geo_test import remove_excess_polygon, check_cross_polygon, get_intersecting_polygons


class Sentinel2overlapTest(unittest.TestCase):
    def test_suitable_regions(self):
        region = 'kharkiv_region.geojson'
        sentinel = "sentinel2_tiles.geojson"
        with open('data_for_tests/suitable_regions_test_valid.geojson') as geojson_res:
            expected_response = json.load(geojson_res)
        test_request, reg = get_intersecting_polygons(sentinel, region)
        val = {}
        val["type"] = "FeatureCollection"
        val["features"] = test_request

        self.assertEqual(val, expected_response)

    def test_remove_excess_polygon(self):
        sentinel = "sentinel2_tiles.geojson"
        poly_reg = 'data_for_tests/excess_ut_region.geojson'
        res_poly, reg = get_intersecting_polygons(sentinel, poly_reg)
        test_request = remove_excess_polygon(res_poly, reg)
        test_request_name = test_request[0]["properties"]["Name"]
        self.assertEqual(test_request_name, "37UEQ")

    def test_check_cross_polygon(self):
        sentinel = "sentinel2_tiles.geojson"
        poly_reg = 'data_for_tests/cross_region_test.geojson'
        res_poly, reg = get_intersecting_polygons(sentinel, poly_reg)
        test_request = check_cross_polygon(res_poly, reg)
        test_request_name = test_request[0]["properties"]["Name"]
        self.assertEqual(test_request_name, "37UDQ")


if __name__ == '__main__':
    unittest.main()
