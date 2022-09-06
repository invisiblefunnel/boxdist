import math
import os
import unittest

from haversine import haversine, Unit
import geojson

from boxdist import geodetic_box_dist, planar_box_dist


class TestBoxDist(unittest.TestCase):
    def setUp(self):
        self.rect, self.cases = read_cases()
        # Expect less than 5cm delta from the haversine package
        self.delta = 5.0 / 100

    def test_geodetic_box_dist_inside(self):
        lon, lat = self.cases["inside"]
        minx, miny, maxx, maxy = self.rect

        actual = geodetic_box_dist(lon, lat, minx, miny, maxx, maxy)
        expected = 0

        self.assertEqual(expected, actual)

    def test_geodetic_box_dist_north(self):
        lon, lat = self.cases["north"]
        minx, miny, maxx, maxy = self.rect

        actual = geodetic_box_dist(lon, lat, minx, miny, maxx, maxy)
        expected = haversine((lat, lon), (maxy, lon), unit=Unit.METERS)

        self.assertAlmostEqual(expected, actual, delta=self.delta)

    def test_geodetic_box_dist_north_east(self):
        lon, lat = self.cases["north-east"]
        minx, miny, maxx, maxy = self.rect

        actual = geodetic_box_dist(lon, lat, minx, miny, maxx, maxy)
        expected = haversine((lat, lon), (maxy, maxx), unit=Unit.METERS)

        self.assertAlmostEqual(expected, actual, delta=self.delta)

    def test_geodetic_box_dist_east(self):
        lon, lat = self.cases["east"]
        minx, miny, maxx, maxy = self.rect

        actual = geodetic_box_dist(lon, lat, minx, miny, maxx, maxy)
        expected = haversine((lat, lon), (lat, maxx), unit=Unit.METERS)

        self.assertAlmostEqual(expected, actual, delta=self.delta)

    def test_geodetic_box_dist_south_east(self):
        lon, lat = self.cases["south-east"]
        minx, miny, maxx, maxy = self.rect

        actual = geodetic_box_dist(lon, lat, minx, miny, maxx, maxy)
        expected = haversine((lat, lon), (miny, maxx), unit=Unit.METERS)

        self.assertAlmostEqual(expected, actual, delta=self.delta)

    def test_geodetic_box_dist_south(self):
        lon, lat = self.cases["south"]
        minx, miny, maxx, maxy = self.rect

        actual = geodetic_box_dist(lon, lat, minx, miny, maxx, maxy)
        expected = haversine((lat, lon), (miny, lon), unit=Unit.METERS)

        self.assertAlmostEqual(expected, actual, delta=self.delta)

    def test_geodetic_box_dist_south_west(self):
        lon, lat = self.cases["south-west"]
        minx, miny, maxx, maxy = self.rect

        actual = geodetic_box_dist(lon, lat, minx, miny, maxx, maxy)
        expected = haversine((lat, lon), (miny, minx), unit=Unit.METERS)

        self.assertAlmostEqual(expected, actual, delta=self.delta)

    def test_geodetic_box_dist_west(self):
        lon, lat = self.cases["west"]
        minx, miny, maxx, maxy = self.rect

        actual = geodetic_box_dist(lon, lat, minx, miny, maxx, maxy)
        expected = haversine((lat, lon), (lat, minx), unit=Unit.METERS)

        self.assertAlmostEqual(expected, actual, delta=self.delta)

    def test_geodetic_box_dist_north_west(self):
        lon, lat = self.cases["north-west"]
        minx, miny, maxx, maxy = self.rect

        actual = geodetic_box_dist(lon, lat, minx, miny, maxx, maxy)
        expected = haversine((lat, lon), (maxy, minx), unit=Unit.METERS)

        self.assertAlmostEqual(expected, actual, delta=self.delta)

    def test_planar_box_dist(self):
        minx = 0
        miny = 0
        maxx = 2
        maxy = 2

        midx = (maxx - minx) / 2
        midy = (maxy - miny) / 2

        # inside
        self.assertEqual(0, planar_box_dist(midx, midy, minx, miny, maxx, maxy))
        # top
        self.assertEqual(1, planar_box_dist(midx, maxy + 1, minx, miny, maxx, maxy))
        # top right
        self.assertEqual(2, planar_box_dist(maxx + 1, maxy + 1, minx, miny, maxx, maxy))
        # right
        self.assertEqual(1, planar_box_dist(maxx + 1, midy, minx, miny, maxx, maxy))
        # bottom right
        self.assertEqual(2, planar_box_dist(maxx + 1, miny - 1, minx, miny, maxx, maxy))
        # bottom
        self.assertEqual(1, planar_box_dist(midx, miny - 1, minx, miny, maxx, maxy))
        # bottom left
        self.assertEqual(2, planar_box_dist(minx - 1, miny - 1, minx, miny, maxx, maxy))
        # left
        self.assertEqual(1, planar_box_dist(minx - 1, midy, minx, miny, maxx, maxy))
        # top right
        self.assertEqual(2, planar_box_dist(minx - 1, maxy + 1, minx, miny, maxx, maxy))


def read_cases():
    cases_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "cases.geojson",
    )

    cases = {}
    minx = math.inf
    miny = math.inf
    maxx = -math.inf
    maxy = -math.inf
    with open(cases_path, "r") as f:
        fc = geojson.loads(f.read())
        for feature in fc.features:
            if feature.geometry.type == "Polygon":
                for x, y in geojson.coords(feature):
                    minx = min(minx, x)
                    miny = min(miny, y)
                    maxx = max(maxx, x)
                    maxy = max(maxy, y)
            else:
                name = feature.properties["name"]
                cases[name] = tuple(feature.geometry.coordinates)
    return (minx, miny, maxx, maxy), cases
