from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class District:
    id: str
    city_id: str
    region_id: str
    name_ar: str
    name_en: str

@dataclass
class City:
    id: str
    region_id: str
    name_ar: str
    name_en: str
    center: Optional[str] = None
    districts: Dict[str, District] = field(default_factory=dict)

@dataclass
class Region:
    id: str
    code: str
    name_ar: str
    name_en: str
    capital_city_id: Optional[str] = None
    population: Optional[int] = None
    center: Optional[str] = None
    cities: Dict[str, City] = field(default_factory=dict)

