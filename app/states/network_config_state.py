import reflex as rx
from typing import Literal, TypedDict
import uuid
import logging

TransportMode = Literal["Parcel", "LTL", "TL"]


class TransportCost(TypedDict):
    mode: TransportMode
    cost_per_mile: float


class TruckCapacity(TypedDict):
    max_volume_cuft: float
    max_weight_lbs: float


class InboundSource(TypedDict):
    source_id: str
    name: str
    location: str


class EdgeOverride(TypedDict):
    override_id: str
    from_node_id: str
    to_node_id: str
    cost_per_mile: float


TOP_25_US_PORTS = [
    {"name": "Port of Houston, TX", "location": "Houston, TX"},
    {"name": "Port of South Louisiana, LA", "location": "LaPlace, LA"},
    {"name": "Port of Corpus Christi, TX", "location": "Corpus Christi, TX"},
    {"name": "Port of New York and New Jersey", "location": "New York, NY"},
    {"name": "Port of Beaumont, TX", "location": "Beaumont, TX"},
    {"name": "Port of New Orleans, LA", "location": "New Orleans, LA"},
    {"name": "Port of Long Beach, CA", "location": "Long Beach, CA"},
    {"name": "Port of Virginia (Hampton Roads)", "location": "Norfolk, VA"},
    {"name": "Port of Los Angeles, CA", "location": "Los Angeles, CA"},
    {"name": "Port of Baton Rouge, LA", "location": "Port Allen, LA"},
    {"name": "Port of Mobile, AL", "location": "Mobile, AL"},
    {"name": "Port of Texas City, TX", "location": "Texas City, TX"},
    {"name": "Port of Savannah, GA", "location": "Savannah, GA"},
    {"name": "Port of Lake Charles, LA", "location": "Lake Charles, LA"},
    {"name": "Port of Plaquemines, LA", "location": "Plaquemines Parish, LA"},
    {"name": "Port of Baltimore, MD", "location": "Baltimore, MD"},
    {"name": "Port of Philadelphia, PA", "location": "Philadelphia, PA"},
    {"name": "Port of Freeport, TX", "location": "Freeport, TX"},
    {"name": "Port of Charleston, SC", "location": "Charleston, SC"},
    {"name": "Port of Seattle/Tacoma, WA (NWSA)", "location": "Seattle/Tacoma, WA"},
    {"name": "Port of Port Arthur, TX", "location": "Port Arthur, TX"},
    {"name": "Port of Oakland, CA", "location": "Oakland, CA"},
    {"name": "Port of Jacksonville, FL", "location": "Jacksonville, FL"},
    {"name": "Port of Miami, FL", "location": "Miami, FL"},
    {"name": "Port of Greater Port Everglades, FL", "location": "Fort Lauderdale, FL"},
]


class NetworkConfigState(rx.State):
    transport_costs: list[TransportCost] = [
        {"mode": "Parcel", "cost_per_mile": 0.5},
        {"mode": "LTL", "cost_per_mile": 2.0},
        {"mode": "TL", "cost_per_mile": 3.0},
    ]
    truck_capacity: TruckCapacity = {
        "max_volume_cuft": 2000.0,
        "max_weight_lbs": 44000.0,
    }
    inbound_sources: list[InboundSource] = [
        {
            "source_id": str(uuid.uuid4()),
            "name": port["name"],
            "location": port["location"],
        }
        for port in TOP_25_US_PORTS
    ]
    edge_overrides: list[EdgeOverride] = []

    @rx.event
    def update_transport_cost(self, mode: TransportMode, cost: str):
        try:
            cost_float = float(cost)
            for i, tc in enumerate(self.transport_costs):
                if tc["mode"] == mode:
                    self.transport_costs[i]["cost_per_mile"] = cost_float
                    return
        except ValueError as e:
            logging.exception(f"Error: {e}")
            return rx.toast.error("Invalid cost value.")

    @rx.event
    def update_truck_capacity(self, field: str, value: str):
        try:
            value_float = float(value)
            if field in self.truck_capacity:
                self.truck_capacity[field] = value_float
        except ValueError as e:
            logging.exception(f"Error: {e}")
            return rx.toast.error("Invalid capacity value.")