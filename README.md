## Скрипт на языке Python для поиска полигонов сетки спутника Sentinel2, которые покрывают заданную пользователем область

* Для запуска скрипта из консоли по исходному условию для региона из примера (Харькова) задействуется команда 
`python geo_test.py kharkiv_region.geojson Merged_Polygon.json`

* Для проверки на полное вхождение заданной области исключительно в область пересеченич полигонов:
`python geo_test.py cross_test.geojson Merged_Polygon.json`

* Для проверки на покрытия заданной области только областью перекрытия с
соседним полигоном:
`python geo_test.py excess_test.geojson Merged_Polygon.json`

* Для запуска unit-тестов:
`python -m unittest unittests.py`
