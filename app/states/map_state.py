import reflex as rx
from reflex_enterprise.components.map.types import LatLng, latlng
import uuid
from typing import Literal, TypedDict

FacilityType = Literal["DC", "Cross-dock", "Last-mile", "Retail"]


class Facility(TypedDict):
    facility_id: str
    facility_type: FacilityType
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


FACILITY_COLORS = {
    "DC": "#1E90FF",
    "Cross-dock": "#FF4500",
    "Last-mile": "#32CD32",
    "Retail": "#FFD700",
}


class MapState(rx.State):
    center: LatLng = latlng(lat=39.8283, lng=-98.5795)
    zoom: float = 4.0
    facilities: list[Facility] = []
    selected_facility_type: FacilityType = "DC"

    @rx.event
    def add_facility(self, event: dict):
        lat = event["latlng"]["lat"]
        lng = event["latlng"]["lng"]
        facility_type_count = sum(
            (
                1
                for f in self.facilities
                if f["facility_type"] == self.selected_facility_type
            )
        )
        site_name = (
            f"{self.selected_facility_type} {chr(ord('A') + facility_type_count)}"
        )
        new_facility = Facility(
            facility_id=str(uuid.uuid4()),
            facility_type=self.selected_facility_type,
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
        self.facilities.extend(facilities)

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

    @rx.var
    def facility_markers(self) -> list[dict]:
        markers = []
        for facility in self.facilities:
            if facility["is_active"]:
                markers.append(
                    {
                        "id": facility["facility_id"],
                        "position": latlng(
                            lat=facility["latitude"], lng=facility["longitude"]
                        ),
                        "facility_id": facility["facility_id"],
                        "color": FACILITY_COLORS[facility["facility_type"]],
                        "tooltip": facility["site_name"],
                    }
                )
        return markers