"""
Pipe Standards Pro v12 - Data Models
Data structures and calculations for pipes, bends, and flanges
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import math


@dataclass
class PipeSpec:
    """Pipe specification data"""
    nps_or_dn: str          # Nominal size (e.g., "2" or "50")
    od: float               # Outer diameter
    wall_thickness: float   # Wall thickness
    schedule: str           # Schedule or thickness designation
    standard: str           # "ASME" or "DIN"
    
    @property
    def id(self) -> float:
        """Inner diameter"""
        return self.od - 2 * self.wall_thickness
    
    @property
    def cross_section_area(self) -> float:
        """Inner cross-sectional area"""
        return math.pi * (self.id / 2) ** 2
    
    @property
    def metal_area(self) -> float:
        """Metal cross-sectional area"""
        outer_area = math.pi * (self.od / 2) ** 2
        inner_area = math.pi * (self.id / 2) ** 2
        return outer_area - inner_area


@dataclass
class BendSpec:
    """Bend/elbow specification data"""
    nps_or_dn: str
    angle: float            # Bend angle in degrees (90, 45, etc.)
    radius_type: str        # "LR" (Long Radius) or "SR" (Short Radius)
    radius: float           # Center-line radius
    od: float               # Pipe outer diameter
    wall_thickness: float
    standard: str           # "ASME" or "DIN"
    
    @property
    def arc_length(self) -> float:
        """Center-line arc length"""
        return 2 * math.pi * self.radius * (self.angle / 360)


@dataclass
class FlangeSpec:
    """Flange specification data"""
    nps_or_dn: str
    pressure_class: str     # "150", "300", "600" (ASME) or "10", "16", "40" (DIN)
    od: float               # Outer diameter
    thickness: float        # Flange thickness
    bolt_circle_dia: float  # Bolt circle diameter
    num_bolts: int          # Number of bolts
    bolt_size: float        # Bolt diameter
    standard: str           # "ASME" or "DIN"
    flange_type: str = "WN" # WN (Weld Neck), SO (Slip-On), BL (Blind), etc.


@dataclass
class FlowCalc:
    """Flow calculation results"""
    pipe_id: float              # Pipe inner diameter
    flow_rate: float            # Volumetric flow rate
    velocity: float             # Flow velocity
    reynolds_number: float      # Reynolds number
    flow_regime: str            # "Laminar" or "Turbulent"
    pressure_drop: Optional[float] = None  # Pressure drop per unit length


def calculate_flow_velocity(flow_rate: float, inner_diameter: float) -> float:
    """
    Calculate flow velocity
    
    Args:
        flow_rate: m³/s
        inner_diameter: meters
    
    Returns:
        velocity in m/s
    """
    area = math.pi * (inner_diameter / 2) ** 2
    return flow_rate / area if area > 0 else 0


def calculate_reynolds_number(velocity: float, diameter: float, 
                              kinematic_viscosity: float = 1.004e-6) -> float:
    """
    Calculate Reynolds number
    
    Args:
        velocity: m/s
        diameter: meters
        kinematic_viscosity: m²/s (default: water at 20°C)
    
    Returns:
        Reynolds number (dimensionless)
    """
    return (velocity * diameter) / kinematic_viscosity


def calculate_pressure_drop(velocity: float, diameter: float, length: float,
                           roughness: float = 0.000045, 
                           density: float = 1000) -> float:
    """
    Calculate pressure drop using Darcy-Weisbach equation
    
    Args:
        velocity: m/s
        diameter: meters
        length: meters
        roughness: meters (default: steel pipe)
        density: kg/m³ (default: water)
    
    Returns:
        pressure drop in Pa
    """
    # Calculate Reynolds number
    re = calculate_reynolds_number(velocity, diameter)
    
    # Calculate friction factor using Colebrook-White approximation
    if re < 2300:  # Laminar flow
        f = 64 / re
    else:  # Turbulent flow - Swamee-Jain approximation
        relative_roughness = roughness / diameter
        f = 0.25 / (math.log10(relative_roughness / 3.7 + 5.74 / (re ** 0.9))) ** 2
    
    # Darcy-Weisbach equation
    return f * (length / diameter) * (density * velocity ** 2) / 2


def get_flow_regime(reynolds_number: float) -> str:
    """Determine flow regime based on Reynolds number"""
    if reynolds_number < 2300:
        return "Laminar"
    elif reynolds_number < 4000:
        return "Transitional"
    else:
        return "Turbulent"


def convert_units(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert between common units
    
    Args:
        value: Value to convert
        from_unit: Source unit ("mm", "inch", "m", "ft", etc.)
        to_unit: Target unit
    
    Returns:
        Converted value
    """
    # Length conversions to meters
    to_meters = {
        "mm": 0.001,
        "cm": 0.01,
        "m": 1.0,
        "inch": 0.0254,
        "ft": 0.3048,
    }
    
    if from_unit in to_meters and to_unit in to_meters:
        return value * to_meters[from_unit] / to_meters[to_unit]
    
    return value  # No conversion possible


class PipeDatabase:
    """Database helper for pipe standards"""
    
    def __init__(self, asme_data: Dict, din_data: Dict):
        self.asme_data = asme_data
        self.din_data = din_data
    
    def get_pipe_spec(self, nps_or_dn: str, schedule: str, 
                      standard: str) -> Optional[PipeSpec]:
        """Get pipe specification"""
        data = self.asme_data if standard == "ASME" else self.din_data
        
        if nps_or_dn not in data:
            return None
        
        od, schedules = data[nps_or_dn]
        
        if standard == "ASME":
            if schedule not in schedules:
                return None
            wall = schedules[schedule]
        else:  # DIN
            if schedule not in schedules:
                return None
            wall = schedule
        
        return PipeSpec(
            nps_or_dn=nps_or_dn,
            od=od,
            wall_thickness=float(wall),
            schedule=str(schedule),
            standard=standard
        )
    
    def get_available_schedules(self, nps_or_dn: str, 
                               standard: str) -> List[str]:
        """Get available schedules for a pipe size"""
        data = self.asme_data if standard == "ASME" else self.din_data
        
        if nps_or_dn not in data:
            return []
        
        _, schedules = data[nps_or_dn]
        
        if standard == "ASME":
            return list(schedules.keys())
        else:  # DIN - return thickness values as strings
            return [str(t) for t in schedules]
    
    def get_all_sizes(self, standard: str) -> List[str]:
        """Get all available pipe sizes for a standard"""
        data = self.asme_data if standard == "ASME" else self.din_data
        return list(data.keys())
    
    def search_pipes(self, query: str, standard: str) -> List[str]:
        """Search for pipes matching query"""
        all_sizes = self.get_all_sizes(standard)
        query_lower = query.lower()
        return [size for size in all_sizes if query_lower in size.lower()]
