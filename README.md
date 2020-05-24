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

####Заметки
* Была переписана часть кода для поиска пересечений области с большой базой
геометрий, задействован метод __overlay_intersection_ пакета _geopandas_ [GitHub](https://github.com/geopandas/geopandas/blob/master/geopandas/tools/overlay.py), который использует rtree пространственный индекс "под капотом".
* Благодаря данному изменению скрипт стал работать примерно на 1,5с быстрее, чем в прошлом релизе.