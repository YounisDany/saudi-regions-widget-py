# توثيق مكتبة Saudi Regions Widget (Python)

مرحباً بك في توثيق مكتبة `saudi-regions-widget-py`، وهي مكتبة Python قوية وسهلة الاستخدام مصممة لتوفير وصول مبسط إلى بيانات المناطق والمدن والأحياء في المملكة العربية السعودية.

هذه المكتبة هي تحويل لمكتبة JavaScript الأصلية [YounisDany/saudi-regions-widget](https://github.com/YounisDany/saudi-regions-widget)، وتهدف إلى تمكين مطوري Python من دمج البيانات الجغرافية السعودية بسهولة في تطبيقاتهم.

## جدول المحتويات

1.  [الميزات الرئيسية](#الميزات-الرئيسية)
2.  [التثبيت](#التثبيت)
3.  [الاستخدام](#الاستخدام)
    *   [التهيئة](#التهيئة)
    *   [الحصول على المناطق](#الحصول-على-المناطق)
    *   [الحصول على المدن](#الحصول-على-المدن)
    *   [الحصول على الأحياء](#الحصول-على-الأحياء-يتطلب-data_levelcomplete)
    *   [البحث](#البحث)
    *   [تغيير اللغة](#تغيير-اللغة)
4.  [مرجع API](#مرجع-api)
5.  [المساهمة](#المساهمة)
6.  [الترخيص](#الترخيص)
7.  [المؤلف](#المؤلف)
8.  [English Documentation](https://github.com/YounisDany/saudi-regions-widget-py/blob/master/docs/en/index.md)

## الميزات الرئيسية

*   **بيانات شاملة**: تتضمن بيانات لجميع 13 منطقة، بالإضافة إلى المدن والأحياء (حسب مستوى البيانات المحدد).
*   **مستويات تحميل البيانات المرنة**: إمكانية تحميل بيانات المناطق فقط (`regions`)، أو المناطق والمدن (`regions-cities`)، أو البيانات الكاملة (`complete`) التي تشمل المناطق والمدن والأحياء.
*   **دعم اللغتين**: أسماء المناطق والمدن والأحياء متوفرة باللغتين العربية والإنجليزية، مع إمكانية التبديل بينهما بسهولة.
*   **وظائف البحث القوية**: البحث عن المناطق والمدن والأحياء بالاسم باللغتين العربية والإنجليزية.
*   **سهولة الاستخدام**: واجهة برمجة تطبيقات (API) بسيطة ومباشرة، مصممة لتسهيل دمج البيانات في تطبيقات Python.

## التثبيت

يمكنك تثبيت المكتبة بسهولة باستخدام pip:

```bash
pip install saudi-regions-widget-py
```

## الاستخدام

### التهيئة

قم بتهيئة المكتبة مع تحديد مستوى البيانات واللغة الافتراضية. مستوى البيانات الافتراضي هو `regions-cities` واللغة الافتراضية هي `ar` (العربية).

```python
from saudi_regions import SaudiRegions

# تهيئة المكتبة لتحميل المناطق والمدن باللغة العربية (افتراضي)
regions_data = SaudiRegions(data_level="regions-cities", language="ar")

# تهيئة المكتبة لتحميل البيانات الكاملة باللغة الإنجليزية
# regions_data_complete_en = SaudiRegions(data_level="complete", language="en")
```

### الحصول على المناطق

يمكنك استرداد قائمة بجميع المناطق أو البحث عن منطقة محددة بواسطة معرفها.

```python
regions = regions_data.get_regions()
print("\nجميع المناطق:")
for region in regions:
    print(f"ID: {region.id}, الاسم (عربي): {region.name_ar}, الاسم (إنجليزي): {region.name_en}")

# الحصول على منطقة معينة بواسطة المعرف (مثلاً، منطقة الرياض بمعرف "1")
riyadh_region = regions_data.get_region_by_id("1")
if riyadh_region:
    print(f"\nمنطقة الرياض: {riyadh_region.name_ar}")
```

### الحصول على المدن

يمكنك الحصول على جميع المدن، أو المدن التابعة لمنطقة معينة، أو مدينة محددة بواسطة معرفها.

```python
# الحصول على جميع المدن (متاحة فقط إذا كان data_level هو \'regions-cities\' أو \'complete\')
cities = regions_data.get_cities()
# print("\nجميع المدن:")
# for city in cities:
#     print(f"ID: {city.id}, الاسم (عربي): {city.name_ar}, معرف المنطقة: {city.region_id}")

# الحصول على مدن منطقة معينة (مثلاً، منطقة الرياض بمعرف "1")
riyadh_cities = regions_data.get_cities(region_id="1")
print(f"\nمدن منطقة الرياض:")
for city in riyadh_cities:
    print(f"  ID: {city.id}, الاسم (عربي): {city.name_ar}")

# الحصول على مدينة معينة بواسطة المعرف (مثلاً، مدينة جدة بمعرف "105")
jiddah_city = regions_data.get_city_by_id("105")
if jiddah_city:
    print(f"\nمدينة جدة: {jiddah_city.name_ar}")
```

### الحصول على الأحياء (يتطلب `data_level="complete"`)

للوصول إلى بيانات الأحياء، يجب تهيئة المكتبة بمستوى البيانات `complete`.

```python
# يجب تهيئة المكتبة بمستوى بيانات "complete" للوصول إلى الأحياء
regions_data_complete = SaudiRegions(data_level="complete", language="ar")

# الحصول على أحياء مدينة معينة (مثلاً، مدينة الرياض بمعرف "101")
riyadh_districts = regions_data_complete.get_districts(city_id="101")
print(f"\nأحياء مدينة الرياض:")
for district in riyadh_districts:
    print(f"  ID: {district.id}, الاسم (عربي): {district.name_ar}")

# الحصول على حي معين بواسطة المعرف (مثلاً، حي الملز بمعرف "1010101")
malaz_district = regions_data_complete.get_district_by_id("1010101")
if malaz_district:
    print(f"\nحي الملز: {malaz_district.name_ar}")
```

### البحث

يمكنك البحث عن المناطق أو المدن أو الأحياء باستخدام استعلام نصي.

```python
# البحث عن "الرياض" في جميع الأنواع (مناطق ومدن)
search_results = regions_data.search("الرياض")
print(f"\nنتائج البحث عن \'الرياض\':")
for result in search_results:
    print(f"  النوع: {result["type"].capitalize()}, الاسم (عربي): {result["data"].name_ar}")

# البحث عن المدن فقط
city_search_results = regions_data.search("جدة", search_type="cities")
print(f"\nنتائج البحث عن \'جدة\' (المدن فقط):")
for result in city_search_results:
    print(f"  الاسم (عربي): {result["data"].name_ar}")
```

### تغيير اللغة

يمكنك تغيير اللغة الافتراضية للمكتبة في أي وقت لاسترداد الأسماء باللغة المطلوبة.

```python
regions_data.set_language("en")
riyadh_region_en = regions_data.get_region_by_id("1")
if riyadh_region_en:
    print(f"\nمنطقة الرياض (باللغة الإنجليزية): {riyadh_region_en.name_en}")
```

## مرجع API

### `class SaudiRegions(data_level='regions-cities', language='ar', data_url=None)`

الفئة الرئيسية للمكتبة.

**المعاملات:**

*   `data_level` (str): مستوى البيانات المراد تحميلها. يمكن أن يكون `regions`، `regions-cities`، أو `complete`. الافتراضي هو `regions-cities`.
*   `language` (str): اللغة الافتراضية للأسماء. يمكن أن تكون `ar` (العربية) أو `en` (الإنجليزية). الافتراضي هو `ar`.
*   `data_url` (str, اختياري): عنوان URL مخصص لتحميل البيانات منه. إذا لم يتم تحديده، سيتم استخدام CDN الافتراضي.

### `get_regions() -> List[Region]`

إرجاع قائمة بجميع كائنات `Region` المحملة.

### `get_region_by_id(region_id: str) -> Optional[Region]`

إرجاع كائن `Region` المطابق للمعرف المحدد، أو `None` إذا لم يتم العثور عليه.

### `get_cities(region_id: Optional[str] = None) -> List[City]`

إرجاع قائمة بجميع كائنات `City` المحملة. إذا تم توفير `region_id`، فسيتم إرجاع المدن التابعة لتلك المنطقة فقط.

### `get_city_by_id(city_id: str) -> Optional[City]`

إرجاع كائن `City` المطابق للمعرف المحدد، أو `None` إذا لم يتم العثور عليه.

### `get_districts(city_id: Optional[str] = None, region_id: Optional[str] = None) -> List[District]`

إرجاع قائمة بجميع كائنات `District` المحملة. يتطلب `data_level="complete"`.
إذا تم توفير `city_id`، فسيتم إرجاع الأحياء التابعة لتلك المدينة فقط.
إذا تم توفير `region_id`، فسيتم إرجاع الأحياء التابعة لتلك المنطقة فقط.

### `get_district_by_id(district_id: str) -> Optional[District]`

إرجاع كائن `District` المطابق للمعرف المحدد، أو `None` إذا لم يتم العثور عليه. يتطلب `data_level="complete"`.

### `search(query: str, search_type: str = 'all') -> List[Dict[str, Union[str, Region, City, District]]]`

البحث عن المناطق أو المدن أو الأحياء بناءً على استعلام نصي.

**المعاملات:**

*   `query` (str): سلسلة البحث.
*   `search_type` (str): نوع الكيانات المراد البحث فيها. يمكن أن يكون `all` (الافتراضي)، `regions`، `cities`، أو `districts`.

**الإرجاع:**

قائمة بالقواميس، حيث يحتوي كل قاموس على مفتاح `type` (يشير إلى نوع الكيان) ومفتاح `data` (يحتوي على كائن `Region` أو `City` أو `District`).

### `set_language(language: str)`

تغيير اللغة الافتراضية للمكتبة (`ar` أو `en`).

### `get_version() -> str`

إرجاع رقم إصدار المكتبة.

## المساهمة

المساهمات مرحب بها! يرجى قراءة [CONTRIBUTING.md](https://github.com/YounisDany/saudi-regions-widget-py/blob/master/CONTRIBUTING.md) لمزيد من التفاصيل.

## الترخيص

هذا المشروع مرخص بموجب ترخيص MIT. انظر ملف [LICENSE](https://github.com/YounisDany/saudi-regions-widget-py/blob/master/LICENSE) لمزيد من التفاصيل.

## المؤلف

**يونس ضاعني**

*   GitHub: [YounisDany](https://github.com/YounisDany)

---
