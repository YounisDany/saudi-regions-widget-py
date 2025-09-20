import pytest
from saudi_regions import SaudiRegions, Region, City, District

# Mock data for testing purposes
MOCK_COMPLETE_DATA = {
    "1": {
        "region": {"id": "1", "code": "01", "name_ar": "الرياض", "name_en": "Riyadh", "capital_city_id": "101"},
        "cities": {
            "101": {"id": "101", "region_id": "1", "name_ar": "الرياض", "name_en": "Riyadh", "center": "24.7136,46.6753",
                      "districts": {
                          "1010101": {"id": "1010101", "city_id": "101", "region_id": "1", "name_ar": "الملز", "name_en": "Al Malaz"},
                          "1010102": {"id": "1010102", "city_id": "101", "region_id": "1", "name_ar": "العليا", "name_en": "Al Olaya"}
                      }}
        }
    },
    "2": {
        "region": {"id": "2", "code": "02", "name_ar": "مكة المكرمة", "name_en": "Makkah Al Mukarramah", "capital_city_id": "105"},
        "cities": {
            "105": {"id": "105", "region_id": "2", "name_ar": "جدة", "name_en": "Jeddah", "center": "21.4858,39.1925",
                      "districts": {
                          "1050101": {"id": "1050101", "city_id": "105", "region_id": "2", "name_ar": "الرويس", "name_en": "Al Ruwais"}
                      }}
        }
    }
}

MOCK_REGIONS_CITIES_DATA = {
    "regions": {
        "1": {"id": "1", "code": "01", "name_ar": "الرياض", "name_en": "Riyadh", "capital_city_id": "101"},
        "2": {"id": "2", "code": "02", "name_ar": "مكة المكرمة", "name_en": "Makkah Al Mukarramah", "capital_city_id": "105"}
    },
    "cities": {
        "101": {"id": "101", "region_id": "1", "name_ar": "الرياض", "name_en": "Riyadh", "center": "24.7136,46.6753"},
        "105": {"id": "105", "region_id": "2", "name_ar": "جدة", "name_en": "Jeddah", "center": "21.4858,39.1925"}
    }
}

MOCK_REGIONS_DATA = {
    "1": {"id": "1", "code": "01", "name_ar": "الرياض", "name_en": "Riyadh", "capital_city_id": "101"},
    "2": {"id": "2", "code": "02", "name_ar": "مكة المكرمة", "name_en": "Makkah Al Mukarramah", "capital_city_id": "105"}
}

# Mock DataLoader to avoid actual HTTP requests during tests
class MockDataLoader:
    def __init__(self, data_url, data_level):
        self.data_url = data_url
        self.data_level = data_level

    def load_data(self):
        if self.data_level == 'complete':
            return MOCK_COMPLETE_DATA
        elif self.data_level == 'regions-cities':
            return MOCK_REGIONS_CITIES_DATA
        elif self.data_level == 'regions':
            return MOCK_REGIONS_DATA
        else:
            raise ValueError("Unknown data level for mock data")

# Patch the DataLoader for testing
import saudi_regions.saudi_regions
saudi_regions.saudi_regions.DataLoader = MockDataLoader


class TestSaudiRegions:

    def test_initialization_default(self):
        sr = SaudiRegions()
        assert sr.data_level == 'regions-cities'
        assert sr.language == 'ar'
        assert len(sr.get_regions()) == 2
        assert len(sr.get_cities()) == 2
        assert len(sr.get_districts()) == 0 # No districts in regions-cities level

    def test_initialization_complete_data(self):
        sr = SaudiRegions(data_level='complete', language='en')
        assert sr.data_level == 'complete'
        assert sr.language == 'en'
        assert len(sr.get_regions()) == 2
        assert len(sr.get_cities()) == 2
        assert len(sr.get_districts()) == 3

    def test_initialization_regions_data(self):
        sr = SaudiRegions(data_level='regions')
        assert sr.data_level == 'regions'
        assert len(sr.get_regions()) == 2
        assert len(sr.get_cities()) == 0 # No cities in regions level
        assert len(sr.get_districts()) == 0

    def test_invalid_data_level(self):
        with pytest.raises(ValueError, match="Invalid data_level"):
            SaudiRegions(data_level='invalid')

    def test_invalid_language(self):
        with pytest.raises(ValueError, match="Invalid language"):
            SaudiRegions(language='fr')

    def test_get_regions(self):
        sr = SaudiRegions()
        regions = sr.get_regions()
        assert len(regions) == 2
        assert any(r.name_ar == 'الرياض' for r in regions)
        assert any(r.name_en == 'Makkah Al Mukarramah' for r in regions)

    def test_get_region_by_id(self):
        sr = SaudiRegions()
        riyadh = sr.get_region_by_id('1')
        assert riyadh is not None
        assert riyadh.name_ar == 'الرياض'
        assert sr.get_region_by_id('99') is None

    def test_get_cities_all(self):
        sr = SaudiRegions()
        cities = sr.get_cities()
        assert len(cities) == 2
        assert any(c.name_ar == 'الرياض' for c in cities)
        assert any(c.name_en == 'Jeddah' for c in cities)

    def test_get_cities_by_region_id(self):
        sr = SaudiRegions()
        riyadh_cities = sr.get_cities(region_id='1')
        assert len(riyadh_cities) == 1
        assert riyadh_cities[0].name_ar == 'الرياض'

        makkah_cities = sr.get_cities(region_id='2')
        assert len(makkah_cities) == 1
        assert makkah_cities[0].name_en == 'Jeddah'

        assert sr.get_cities(region_id='99') == []

    def test_get_city_by_id(self):
        sr = SaudiRegions()
        riyadh_city = sr.get_city_by_id('101')
        assert riyadh_city is not None
        assert riyadh_city.name_ar == 'الرياض'
        assert sr.get_city_by_id('999') is None

    def test_get_districts_complete_data(self):
        sr = SaudiRegions(data_level='complete')
        districts = sr.get_districts()
        assert len(districts) == 3
        assert any(d.name_ar == 'الملز' for d in districts)

    def test_get_districts_by_city_id(self):
        sr = SaudiRegions(data_level='complete')
        riyadh_districts = sr.get_districts(city_id='101')
        assert len(riyadh_districts) == 2
        assert any(d.name_ar == 'الملز' for d in riyadh_districts)

        jeddah_districts = sr.get_districts(city_id='105')
        assert len(jeddah_districts) == 1
        assert jeddah_districts[0].name_en == 'Al Ruwais'

        assert sr.get_districts(city_id='999') == []

    def test_get_districts_by_region_id(self):
        sr = SaudiRegions(data_level='complete')
        riyadh_region_districts = sr.get_districts(region_id='1')
        assert len(riyadh_region_districts) == 2
        assert any(d.name_ar == 'الملز' for d in riyadh_region_districts)

        makkah_region_districts = sr.get_districts(region_id='2')
        assert len(makkah_region_districts) == 1
        assert makkah_region_districts[0].name_en == 'Al Ruwais'

        assert sr.get_districts(region_id='99') == []

    def test_search_regions_ar(self):
        sr = SaudiRegions(language='ar')
        results = sr.search('الرياض', search_type='regions')
        assert len(results) == 1
        assert results[0]['type'] == 'region'
        assert results[0]['data'].name_ar == 'الرياض'

    def test_search_regions_en(self):
        sr = SaudiRegions(language='en')
        results = sr.search('Riyadh', search_type='regions')
        assert len(results) == 1
        assert results[0]['type'] == 'region'
        assert results[0]['data'].name_en == 'Riyadh'

    def test_search_cities_ar(self):
        sr = SaudiRegions(data_level='regions-cities', language='ar')
        results = sr.search('جدة', search_type='cities')
        assert len(results) == 1
        assert results[0]['type'] == 'city'
        assert results[0]['data'].name_ar == 'جدة'

    def test_search_cities_en(self):
        sr = SaudiRegions(data_level='regions-cities', language='en')
        results = sr.search('Jeddah', search_type='cities')
        assert len(results) == 1
        assert results[0]['type'] == 'city'
        assert results[0]['data'].name_en == 'Jeddah'

    def test_search_districts_ar(self):
        sr = SaudiRegions(data_level='complete', language='ar')
        results = sr.search('الملز', search_type='districts')
        assert len(results) == 1
        assert results[0]['type'] == 'district'
        assert results[0]['data'].name_ar == 'الملز'

    def test_search_all_ar(self):
        sr = SaudiRegions(data_level='complete', language='ar')
        results = sr.search('الرياض', search_type='all')
        assert len(results) == 2 # Riyadh region and Riyadh city
        assert any(r['type'] == 'region' and r['data'].name_ar == 'الرياض' for r in results)
        assert any(r['type'] == 'city' and r['data'].name_ar == 'الرياض' for r in results)

    def test_set_language(self):
        sr = SaudiRegions(language='ar')
        assert sr.language == 'ar'
        sr.set_language('en')
        assert sr.language == 'en'
        with pytest.raises(ValueError):
            sr.set_language('fr')

    def test_get_version(self):
        sr = SaudiRegions()
        assert sr.get_version() == '2.0.0'

    def test_repr(self):
        sr = SaudiRegions()
        assert repr(sr) == "<SaudiRegions data_level='regions-cities', language='ar'>"

    def test_data_level_impact_on_data_access(self):
        sr_regions = SaudiRegions(data_level='regions')
        assert len(sr_regions.get_cities()) == 0
        assert len(sr_regions.get_districts()) == 0

        sr_regions_cities = SaudiRegions(data_level='regions-cities')
        assert len(sr_regions_cities.get_cities()) == 2
        assert len(sr_regions_cities.get_districts()) == 0

        sr_complete = SaudiRegions(data_level='complete')
        assert len(sr_complete.get_cities()) == 2
        assert len(sr_complete.get_districts()) == 3


