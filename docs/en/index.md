# Saudi Regions Widget (Python) Documentation

Welcome to the documentation for `saudi-regions-widget-py`, a powerful and easy-to-use Python library designed to provide simplified access to regions, cities, and districts data in Saudi Arabia.

This library is a Python port of the original JavaScript library [YounisDany/saudi-regions-widget](https://github.com/YounisDany/saudi-regions-widget), aiming to enable Python developers to easily integrate Saudi geographical data into their applications.

## Table of Contents

1.  [Key Features](#key-features)
2.  [Installation](#installation)
3.  [Usage](#usage)
    *   [Initialization](#initialization)
    *   [Getting Regions](#getting-regions)
    *   [Getting Cities](#getting-cities)
    *   [Getting Districts](#getting-districts-requires-data_levelcomplete)
    *   [Searching](#searching)
    *   [Changing Language](#changing-language)
4.  [API Reference](#api-reference)
5.  [Contributing](#contributing)
6.  [License](#license)
7.  [Author](#author)
8.  [توثيق عربي](https://github.com/YounisDany/saudi-regions-widget-py/blob/master/docs/ar/index.md)

## Key Features

*   **Comprehensive Data**: Includes data for all 13 regions, along with cities and districts (depending on the specified data level).
*   **Flexible Data Loading Levels**: Ability to load only regions data (`regions`), regions and cities data (`regions-cities`), or complete data (`complete`) which includes regions, cities, and districts.
*   **Bilingual Support**: Region, city, and district names are available in both Arabic and English, with easy switching between languages.
*   **Powerful Search Functions**: Search for regions, cities, and districts by name in both Arabic and English.
*   **Ease of Use**: A simple and straightforward Application Programming Interface (API), designed to facilitate the integration of geographical data into Python applications.

## Installation

You can easily install the library using pip:

```bash
pip install saudi-regions-widget-py
```

## Usage

### Initialization

Initialize the library by specifying the data level and default language. The default data level is `regions-cities` and the default language is `ar` (Arabic).

```python
from saudi_regions import SaudiRegions

# Initialize the library to load regions and cities data in Arabic (default)
regions_data = SaudiRegions(data_level="regions-cities", language="ar")

# Initialize the library to load complete data in English
# regions_data_complete_en = SaudiRegions(data_level="complete", language="en")
```

### Getting Regions

You can retrieve a list of all regions or search for a specific region by its ID.

```python
regions = regions_data.get_regions()
print("\nAll Regions:")
for region in regions:
    print(f"ID: {region.id}, Name (Arabic): {region.name_ar}, Name (English): {region.name_en}")

# Get a specific region by ID (e.g., Riyadh region with ID "1")
riyadh_region = regions_data.get_region_by_id("1")
if riyadh_region:
    print(f"\nRiyadh Region: {riyadh_region.name_en}")
```

### Getting Cities

You can get all cities, cities belonging to a specific region, or a specific city by its ID.

```python
# Get all cities (only available if data_level is \'regions-cities\' or \'complete\')
cities = regions_data.get_cities()
# print("\nAll Cities:")
# for city in cities:
#     print(f"ID: {city.id}, Name (Arabic): {city.name_ar}, Region ID: {city.region_id}")

# Get cities of a specific region (e.g., Riyadh region with ID "1")
riyadh_cities = regions_data.get_cities(region_id="1")
print(f"\nCities in Riyadh Region:")
for city in riyadh_cities:
    print(f"  ID: {city.id}, Name (English): {city.name_en}")

# Get a specific city by ID (e.g., Jeddah city with ID "105")
jiddah_city = regions_data.get_city_by_id("105")
if jiddah_city:
    print(f"\nJeddah City: {jiddah_city.name_en}")
```

### Getting Districts (requires `data_level="complete"`)

To access district data, the library must be initialized with the `complete` data level.

```python
# The library must be initialized with "complete" data level to access districts
regions_data_complete = SaudiRegions(data_level="complete", language="en")

# Get districts of a specific city (e.g., Riyadh city with ID "101")
riyadh_districts = regions_data_complete.get_districts(city_id="101")
print(f"\nDistricts in Riyadh City:")
for district in riyadh_districts:
    print(f"  ID: {district.id}, Name (English): {district.name_en}")

# Get a specific district by ID (e.g., Al Malaz district with ID "1010101")
malaz_district = regions_data_complete.get_district_by_id("1010101")
if malaz_district:
    print(f"\nAl Malaz District: {malaz_district.name_en}")
```

### Searching

You can search for regions, cities, or districts using a text query.

```python
# Search for "Riyadh" in all types (regions and cities)
search_results = regions_data.search("Riyadh")
print(f"\nSearch results for \'Riyadh\':")
for result in search_results:
    print(f"  Type: {result["type"].capitalize()}, Name (English): {result["data"].name_en}")

# Search for cities only
city_search_results = regions_data.search("Jeddah", search_type="cities")
print(f"\nSearch results for \'Jeddah\' (cities only):")
for result in city_search_results:
    print(f"  Name (English): {result["data"].name_en}")
```

### Changing Language

You can change the default language of the library at any time to retrieve names in the desired language.

```python
regions_data.set_language("ar")
riyadh_region_ar = regions_data.get_region_by_id("1")
if riyadh_region_ar:
    print(f"\nRiyadh Region (in Arabic): {riyadh_region_ar.name_ar}")
```

## API Reference

### `class SaudiRegions(data_level=\'regions-cities\', language=\'ar\', data_url=None)`

The main class of the library.

**Parameters:**

*   `data_level` (str): The data level to load. Can be `regions`, `regions-cities`, or `complete`. Default is `regions-cities`.
*   `language` (str): The default language for names. Can be `ar` (Arabic) or `en` (English). Default is `ar`.
*   `data_url` (str, optional): A custom URL to load data from. If not specified, the default CDN will be used.

### `get_regions() -> List[Region]`

Returns a list of all loaded `Region` objects.

### `get_region_by_id(region_id: str) -> Optional[Region]`

Returns the `Region` object matching the specified ID, or `None` if not found.

### `get_cities(region_id: Optional[str] = None) -> List[City]`

Returns a list of all loaded `City` objects. If `region_id` is provided, only cities belonging to that region will be returned.

### `get_city_by_id(city_id: str) -> Optional[City]`

Returns the `City` object matching the specified ID, or `None` if not found.

### `get_districts(city_id: Optional[str] = None, region_id: Optional[str] = None) -> List[District]`

Returns a list of all loaded `District` objects. Requires `data_level="complete"`.
If `city_id` is provided, only districts belonging to that city will be returned.
If `region_id` is provided, only districts belonging to that region will be returned.

### `get_district_by_id(district_id: str) -> Optional[District]`

Returns the `District` object matching the specified ID, or `None` if not found. Requires `data_level="complete"`.

### `search(query: str, search_type: str = \'all\') -> List[Dict[str, Union[str, Region, City, District]]]`

Searches for regions, cities, or districts based on a text query.

**Parameters:**

*   `query` (str): The search string.
*   `search_type` (str): The type of entities to search within. Can be `all` (default), `regions`, `cities`, or `districts`.

**Returns:**

A list of dictionaries, where each dictionary contains a `type` key (indicating the entity type) and a `data` key (containing the `Region`, `City`, or `District` object).

### `set_language(language: str)`

Changes the default language of the library (`ar` or `en`).

### `get_version() -> str`

Returns the library's version number.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](https://github.com/YounisDany/saudi-regions-widget-py/blob/master/CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/YounisDany/saudi-regions-widget-py/blob/master/LICENSE) file for more details.

## Author

**Younis Dany**

*   GitHub: [YounisDany](https://github.com/YounisDany)

---
