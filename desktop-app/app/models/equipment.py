from dataclasses import dataclass
from typing import Dict, List

@dataclass
class EquipmentRow:
    name: str
    type: str
    flowrate: float
    pressure: float
    temperature: float

@dataclass
class DatasetSummary:
    total_count: int
    avg_flowrate: float
    avg_pressure: float
    avg_temperature: float

@dataclass
class Dataset:
    id: int
    filename: str
    uploaded_at: str
    summary: DatasetSummary
    type_distribution: Dict[str, int]
    rows: List[EquipmentRow]
