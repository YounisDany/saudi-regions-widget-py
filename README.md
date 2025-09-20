# Saudi Regions Widget (Python)

مكتبة Python توفر واجهة برمجية سهلة الاستخدام للوصول إلى بيانات المناطق والمدن والأحياء في المملكة العربية السعودية. هذه المكتبة هي تحويل لمكتبة JavaScript الأصلية [YounisDany/saudi-regions-widget](https://github.com/YounisDany/saudi-regions-widget).

## الميزات

*   **بيانات شاملة**: تتضمن بيانات لجميع 13 منطقة، بالإضافة إلى المدن والأحياء (حسب مستوى البيانات المحدد).
*   **مستويات تحميل البيانات**: إمكانية تحميل بيانات المناطق فقط، أو المناطق والمدن، أو البيانات الكاملة (مناطق، مدن، أحياء).
*   **دعم اللغتين**: أسماء المناطق والمدن والأحياء متوفرة باللغتين العربية والإنجليزية.
*   **وظائف البحث**: البحث عن المناطق والمدن والأحياء بالاسم.
*   **سهولة الاستخدام**: واجهة برمجة تطبيقات (API) بسيطة ومباشرة.

## التثبيت

يمكنك تثبيت المكتبة باستخدام pip:

```bash
pip install saudi-regions-widget
```

## الاستخدام

### التهيئة

يمكنك تهيئة المكتبة مع تحديد مستوى البيانات واللغة الافتراضية:

```python
from saudi_regions import SaudiRegions

# تهيئة المكتبة لتحميل المناطق والمدن باللغة العربية (افتراضي)
regions_data = SaudiRegions(data_level="regions-cities", language="ar")

# تهيئة المكتبة لتحميل البيانات الكاملة باللغة الإنجليزية
# regions_data_complete_en = SaudiRegions(data_level="complete", language="en")
```

### الحصول على المناطق

```python
regions = regions_data.get_regions()
for region in regions:
    print(f"ID: {region.id}, Name (AR): {region.name_ar}, Name (EN): {region.name_en}")

# الحصول على منطقة معينة بواسطة المعرف
riyadh_region = regions_data.get_region_by_id("1")
if riyadh_region:
    print(f"\nRiyadh Region: {riyadh_region.name_ar}")
```

### الحصول على المدن

```python
# الحصول على جميع المدن
cities = regions_data.get_cities()
# for city in cities:
#     print(f"ID: {city.id}, Name (AR): {city.name_ar}, Region ID: {city.region_id}")

# الحصول على مدن منطقة معينة (مثلاً، منطقة الرياض بمعرف "1")
riyadh_cities = regions_data.get_cities(region_id="1")
print(f"\nCities in Riyadh Region:")
for city in riyadh_cities:
    print(f"  ID: {city.id}, Name (AR): {city.name_ar}")

# الحصول على مدينة معينة بواسطة المعرف
jiddah_city = regions_data.get_city_by_id("105")
if jiddah_city:
    print(f"\nJiddah City: {jiddah_city.name_ar}")
```

### الحصول على الأحياء (يتطلب `data_level="complete"`)

```python
# يجب تهيئة المكتبة بمستوى بيانات "complete" للوصول إلى الأحياء
regions_data_complete = SaudiRegions(data_level="complete", language="ar")

# الحصول على أحياء مدينة معينة (مثلاً، مدينة الرياض بمعرف "101")
riyadh_districts = regions_data_complete.get_districts(city_id="101")
print(f"\nDistricts in Riyadh City:")
for district in riyadh_districts:
    print(f"  ID: {district.id}, Name (AR): {district.name_ar}")

# الحصول على حي معين بواسطة المعرف
malaz_district = regions_data_complete.get_district_by_id("1010101")
if malaz_district:
    print(f"\nMalaz District: {malaz_district.name_ar}")
```

### البحث

```python
# البحث عن "الرياض" في جميع الأنواع
search_results = regions_data.search("الرياض")
print(f"\nSearch results for 'الرياض':")
for result in search_results:
    print(f"  Type: {result["type"].capitalize()}, Name (AR): {result["data"].name_ar}")

# البحث عن المدن فقط
city_search_results = regions_data.search("جدة", search_type="cities")
print(f"\nSearch results for 'جدة' (cities only):")
for result in city_search_results:
    print(f"  Name (AR): {result["data"].name_ar}")
```

### تغيير اللغة

```python
regions_data.set_language("en")
riyadh_region_en = regions_data.get_region_by_id("1")
if riyadh_region_en:
    print(f"\nRiyadh Region (English): {riyadh_region_en.name_en}")
```

## المساهمة

المساهمات مرحب بها! يرجى قراءة [CONTRIBUTING.md](CONTRIBUTING.md) لمزيد من التفاصيل.

## الترخيص

هذا المشروع مرخص بموجب ترخيص MIT. انظر ملف [LICENSE](LICENSE) لمزيد من التفاصيل.

