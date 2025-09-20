from typing import List, Dict, Optional, Union, Any
from .data_loader import DataLoader
from .data_models import Region, City, District

class SaudiRegions:
    DEFAULT_DATA_URL = 'https://cdn.jsdelivr.net/gh/YounisDany/saudi-regions-widget@main/dist/data/'
    SUPPORTED_DATA_LEVELS = ['regions', 'regions-cities', 'complete']
    SUPPORTED_LANGUAGES = ['ar', 'en']

    def __init__(
        self,
        data_level: str = 'regions-cities',
        language: str = 'ar',
        data_url: Optional[str] = None
    ):
        if data_level not in self.SUPPORTED_DATA_LEVELS:
            raise ValueError(f"Invalid data_level: {data_level}. Must be one of {self.SUPPORTED_DATA_LEVELS}")
        if language not in self.SUPPORTED_LANGUAGES:
            raise ValueError(f"Invalid language: {language}. Must be one of {self.SUPPORTED_LANGUAGES}")

        self.data_level = data_level
        self.language = language
        self.data_url = data_url if data_url else self.DEFAULT_DATA_URL
        self._data = None
        self._regions_map: Dict[str, Region] = {}
        self._cities_map: Dict[str, City] = {}
        self._districts_map: Dict[str, District] = {}
        self._version = '2.0.0' # Matching the JS widget version

        self._load_and_process_data()

    def _load_and_process_data(self):
        loader = DataLoader(self.data_url, self.data_level)
        raw_data = loader.load_data()
        self._process_raw_data(raw_data)

    def _process_raw_data(self, raw_data: Dict[str, Any]):
        if self.data_level == 'complete':
            for region_id, region_data in raw_data.items():
                region = Region(
                    id=region_data['region']['id'],
                    code=region_data['region']['code'],
                    name_ar=region_data['region']['name_ar'],
                    name_en=region_data['region']['name_en'],
                    capital_city_id=region_data['region'].get('capital_city_id'),
                    population=region_data['region'].get('population'),
                    center=region_data['region'].get('center')
                )
                self._regions_map[region.id] = region

                for city_id, city_data in region_data['cities'].items():
                    city = City(
                        id=city_data['id'],
                        region_id=city_data['region_id'],
                        name_ar=city_data['name_ar'],
                        name_en=city_data['name_en'],
                        center=city_data.get('center')
                    )
                    region.cities[city.id] = city
                    self._cities_map[city.id] = city

                    for district_id, district_data in city_data['districts'].items():
                        district = District(
                            id=district_data['id'],
                            city_id=district_data['city_id'],
                            region_id=district_data['region_id'],
                            name_ar=district_data['name_ar'],
                            name_en=district_data['name_en']
                        )
                        city.districts[district.id] = district
                        self._districts_map[district.id] = district
        elif self.data_level == 'regions-cities':
            for region_id, region_data in raw_data['regions'].items():
                region = Region(
                    id=region_data['id'],
                    code=region_data['code'],
                    name_ar=region_data['name_ar'],
                    name_en=region_data['name_en'],
                    capital_city_id=region_data.get('capital_city_id'),
                    population=region_data.get('population'),
                    center=region_data.get('center')
                )
                self._regions_map[region.id] = region
            
            for city_id, city_data in raw_data['cities'].items():
                city = City(
                    id=city_data['id'],
                    region_id=city_data['region_id'],
                    name_ar=city_data['name_ar'],
                    name_en=city_data['name_en'],
                    center=city_data.get('center')
                )
                self._cities_map[city.id] = city
                if city.region_id in self._regions_map:
                    self._regions_map[city.region_id].cities[city.id] = city
        elif self.data_level == 'regions':
            for region_id, region_data in raw_data.items():
                region = Region(
                    id=region_data['id'],
                    code=region_data['code'],
                    name_ar=region_data['name_ar'],
                    name_en=region_data['name_en'],
                    capital_city_id=region_data.get('capital_city_id'),
                    population=region_data.get('population'),
                    center=region_data.get('center')
                )
                self._regions_map[region.id] = region

    def get_regions(self) -> List[Region]:
        return list(self._regions_map.values())

    def get_region_by_id(self, region_id: str) -> Optional[Region]:
        return self._regions_map.get(region_id)

    def get_cities(self, region_id: Optional[str] = None) -> List[City]:
        if region_id:
            region = self.get_region_by_id(region_id)
            return list(region.cities.values()) if region else []
        return list(self._cities_map.values())

    def get_city_by_id(self, city_id: str) -> Optional[City]:
        return self._cities_map.get(city_id)

    def get_districts(self, city_id: Optional[str] = None, region_id: Optional[str] = None) -> List[District]:
        if self.data_level != 'complete':
            return [] # Districts are only available at 'complete' data level

        if city_id:
            city = self.get_city_by_id(city_id)
            return list(city.districts.values()) if city else []
        elif region_id:
            region = self.get_region_by_id(region_id)
            if region:
                all_districts = []
                for city in region.cities.values():
                    all_districts.extend(city.districts.values())
                return all_districts
            return [] # Return empty list if region_id does not exist
        return list(self._districts_map.values())

    def get_district_by_id(self, district_id: str) -> Optional[District]:
        return self._districts_map.get(district_id)

    def search(self, query: str, search_type: str = 'all') -> List[Dict[str, Union[str, Region, City, District]]]:
        if not query: return []

        results = []
        search_term = query.lower()

        if search_type == 'all' or search_type == 'regions':
            for region in self._regions_map.values():
                if (self.language == 'ar' and search_term in region.name_ar.lower()) or \
                   (self.language == 'en' and search_term in region.name_en.lower()):
                    results.append({'type': 'region', 'data': region})

        if (search_type == 'all' or search_type == 'cities') and self.data_level in ['regions-cities', 'complete']:
            for city in self._cities_map.values():
                if (self.language == 'ar' and search_term in city.name_ar.lower()) or \
                   (self.language == 'en' and search_term in city.name_en.lower()):
                    results.append({'type': 'city', 'data': city})
        
        if (search_type == 'all' or search_type == 'districts') and self.data_level == 'complete':
            for district in self._districts_map.values():
                if (self.language == 'ar' and search_term in district.name_ar.lower()) or \
                   (self.language == 'en' and search_term in district.name_en.lower()):
                    results.append({'type': 'district', 'data': district})

        return results

    def set_language(self, language: str):
        if language not in self.SUPPORTED_LANGUAGES:
            raise ValueError(f"Invalid language: {language}. Must be one of {self.SUPPORTED_LANGUAGES}")
        self.language = language

    def get_version(self) -> str:
        return self._version

    def __repr__(self):
        return f"<SaudiRegions data_level='{self.data_level}', language='{self.language}'>"

