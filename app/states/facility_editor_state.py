import reflex as rx
from app.states.map_state import MapState, Facility, FacilityType, FACILITY_COLORS
from typing import cast

ALL_FACILITY_TYPES = list(FACILITY_COLORS.keys())


class FacilityEditorState(rx.State):
    selected_facility_id: str | None = None
    edited_facility: Facility | None = None

    @rx.var
    async def selected_facility(self) -> Facility | None:
        if not self.selected_facility_id:
            return None
        map_state = await self.get_state(MapState)
        for f in map_state.facilities:
            if f["facility_id"] == self.selected_facility_id:
                return f
        return None

    @rx.event
    async def select_facility(self, facility_id: str):
        self.selected_facility_id = facility_id
        facility = await self.get_var_value(self.selected_facility)
        if facility:
            self.edited_facility = facility.copy()
        else:
            self.edited_facility = None

    @rx.event
    def handle_edit(self, field: str, value: str):
        if self.edited_facility is not None:
            self.edited_facility[field] = value

    @rx.event
    def toggle_facility_type(self, f_type: str):
        if self.edited_facility is not None:
            current_types = self.edited_facility.get("facility_types", [])
            if f_type in current_types:
                current_types.remove(f_type)
            else:
                current_types.append(cast(FacilityType, f_type))
            self.edited_facility["facility_types"] = current_types

    @rx.event
    async def save_changes(self):
        if self.edited_facility:
            map_state = await self.get_state(MapState)
            yield map_state.update_facility(self.edited_facility)
            self.selected_facility_id = None
            self.edited_facility = None
            yield rx.toast.success("Facility updated successfully.")
        else:
            yield rx.toast.error("No facility selected to save.")