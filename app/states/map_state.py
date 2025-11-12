import reflex as rx
from reflex_enterprise.components.map.types import LatLng, latlng
import uuid
from typing import Literal, TypedDict, cast

FacilityType = Literal[
    "DC", "Cross-dock", "Last-mile", "Retail", "Factory", "Source Warehouse", "Port"
]


class Facility(TypedDict):
    facility_id: str
    facility_types: list[FacilityType]
    site_name: str
    parent_company: str
    street_address: str
    city: str
    state_province: str
    zip5: str
    zip9: str
    country: str
    latitude: float
    longitude: float
    is_active: bool


class FacilityNode(TypedDict):
    node_id: str
    facility_id: str
    facility_type: FacilityType
    site_name: str
    latitude: float
    longitude: float
    is_active: bool


FACILITY_COLORS = {
    "DC": "#1E90FF",
    "Cross-dock": "#FF4500",
    "Last-mile": "#32CD32",
    "Retail": "#FFD700",
    "Factory": "#9370DB",
    "Source Warehouse": "#FF8C00",
    "Port": "#008B8B",
}
DEFAULT_PORTS = [
    {
        "name": "Long Beach",
        "lat": 33.7701,
        "lng": -118.1937,
        "city": "Long Beach",
        "state": "CA",
    },
    {
        "name": "Savannah",
        "lat": 32.0809,
        "lng": -81.0912,
        "city": "Savannah",
        "state": "GA",
    },
    {"name": "NY/NJ", "lat": 40.6692, "lng": -74.0445, "city": "Newark", "state": "NJ"},
    {
        "name": "Seattle/Tacoma",
        "lat": 47.2758,
        "lng": -122.4138,
        "city": "Tacoma",
        "state": "WA",
    },
    {
        "name": "Oakland",
        "lat": 37.7965,
        "lng": -122.2801,
        "city": "Oakland",
        "state": "CA",
    },
    {
        "name": "Baltimore",
        "lat": 39.2667,
        "lng": -76.5833,
        "city": "Baltimore",
        "state": "MD",
    },
    {"name": "Miami", "lat": 25.7741, "lng": -80.1931, "city": "Miami", "state": "FL"},
    {
        "name": "Virginia (Norfolk)",
        "lat": 36.8468,
        "lng": -76.2951,
        "city": "Norfolk",
        "state": "VA",
    },
    {
        "name": "Jacksonville",
        "lat": 30.3322,
        "lng": -81.6557,
        "city": "Jacksonville",
        "state": "FL",
    },
    {
        "name": "Port of Houston",
        "lat": 29.7604,
        "lng": -95.3698,
        "city": "Houston",
        "state": "TX",
    },
]


class MapState(rx.State):
    center: LatLng = latlng(lat=39.8283, lng=-98.5795)
    zoom: float = 4.0
    facilities: list[Facility] = []

    @rx.event
    def on_load(self):
        has_ports = any(
            ("Port" in f.get("facility_types", []) for f in self.facilities)
        )
        if not has_ports:
            for port_data in DEFAULT_PORTS:
                new_port = Facility(
                    facility_id=str(uuid.uuid4()),
                    facility_types=["Port"],
                    site_name=f"{port_data['name']} Port",
                    parent_company="US Port Authority",
                    street_address="",
                    city=port_data["city"],
                    state_province=port_data["state"],
                    zip5="",
                    zip9="",
                    country="USA",
                    latitude=port_data["lat"],
                    longitude=port_data["lng"],
                    is_active=True,
                )
                self.facilities.append(new_port)

    @rx.event
    def add_facility(self, event: dict):
        lat = event["latlng"]["lat"]
        lng = event["latlng"]["lng"]
        facility_type_count = sum(
            (1 for f in self.facilities if "DC" in f["facility_types"])
        )
        site_name = f"New Facility {facility_type_count + 1}"
        new_facility = Facility(
            facility_id=str(uuid.uuid4()),
            facility_types=["DC"],
            site_name=site_name,
            parent_company="Default Co",
            street_address="",
            city="",
            state_province="",
            zip5="",
            zip9="",
            country="USA",
            latitude=lat,
            longitude=lng,
            is_active=True,
        )
        self.facilities.append(new_facility)

    @rx.event
    def add_facilities(self, facilities: list[Facility]):
        migrated_facilities = []
        for f in facilities:
            if "facility_type" in f and "facility_types" not in f:
                f["facility_types"] = [cast(FacilityType, f["facility_type"])]
                del f["facility_type"]
            migrated_facilities.append(f)
        self.facilities.extend(migrated_facilities)

    @rx.event
    def remove_facility(self, facility_id: str):
        self.facilities = [
            f for f in self.facilities if f["facility_id"] != facility_id
        ]

    @rx.event
    def toggle_facility_active(self, facility_id: str):
        for i, facility in enumerate(self.facilities):
            if facility["facility_id"] == facility_id:
                self.facilities[i]["is_active"] = not self.facilities[i]["is_active"]
                break

    @rx.event
    def update_facility_location(self, event: dict):
        facility_id = event["target"]["options"]["facility_id"]
        new_latlng = event["target"]["_latlng"]
        for i, facility in enumerate(self.facilities):
            if facility["facility_id"] == facility_id:
                self.facilities[i]["latitude"] = new_latlng["lat"]
                self.facilities[i]["longitude"] = new_latlng["lng"]
                break

    @rx.event
    def update_facility(self, facility_data: Facility):
        for i, f in enumerate(self.facilities):
            if f["facility_id"] == facility_data["facility_id"]:
                self.facilities[i] = facility_data
                return

    @rx.var
    def facility_markers(self) -> list[dict]:
        markers = []
        for facility in self.facilities:
            if facility["is_active"]:
                color = (
                    FACILITY_COLORS[facility["facility_types"][0]]
                    if facility["facility_types"]
                    else "#808080"
                )
                markers.append(
                    {
                        "id": facility["facility_id"],
                        "position": latlng(
                            lat=facility["latitude"], lng=facility["longitude"]
                        ),
                        "facility_id": facility["facility_id"],
                        "color": color,
                        "tooltip": facility["site_name"],
                    }
                )
        return markers

    @rx.var
    def facility_nodes(self) -> list[FacilityNode]:
        nodes = []
        for facility in self.facilities:
            for f_type in facility["facility_types"]:
                nodes.append(
                    FacilityNode(
                        node_id=f"{facility['facility_id']}_{f_type}",
                        facility_id=facility["facility_id"],
                        facility_type=f_type,
                        site_name=facility["site_name"],
                        latitude=facility["latitude"],
                        longitude=facility["longitude"],
                        is_active=facility["is_active"],
                    )
                )
        return nodes