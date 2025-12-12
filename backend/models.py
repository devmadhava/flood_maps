from pydantic import BaseModel
from pathlib import Path
from whitebox import WhiteboxTools

class LocationRequest(BaseModel):
    lat: float
    lon: float

# SLOPE IN DEGREE
class CheckDamParams(BaseModel):
    wbt: WhiteboxTools
    slope: Path
    spi: Path
    twi: Path
    filled_dem: Path
    check_dam_points: Path
    streams_vector: Path
    class Config:
        arbitrary_types_allowed = True

class Convert3857VectorTo4326(BaseModel):
    vector_3857: Path
    vector_4326: Path