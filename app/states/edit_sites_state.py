import reflex as rx
from app.states.map_state import MapState, Facility


class EditSitesState(rx.State):
    search_query: str = ""
    sort_by: str = "site_name"
    sort_order: str = "asc"

    @rx.event
    async def on_load(self):
        pass

    @rx.event
    def set_sort_column(self, column: str):
        if self.sort_by == column:
            self.sort_order = "desc" if self.sort_order == "asc" else "asc"
        else:
            self.sort_by = column
            self.sort_order = "asc"

    @rx.var
    async def filtered_and_sorted_facilities(self) -> list[Facility]:
        map_state = await self.get_state(MapState)
        facilities = map_state.facilities
        if self.search_query:
            search_lower = self.search_query.lower()
            facilities = [
                f
                for f in facilities
                if search_lower in f["site_name"].lower()
                or any((search_lower in t.lower() for t in f["facility_types"]))
                or search_lower in f["parent_company"].lower()
                or (search_lower in f["street_address"].lower())
                or (search_lower in f["city"].lower())
                or (search_lower in f["state_province"].lower())
                or (search_lower in f["zip5"].lower())
            ]
        reverse = self.sort_order == "desc"

        @rx.event
        def sort_key(f: Facility):
            val = f.get(self.sort_by)
            if self.sort_by == "facility_types":
                return ", ".join(sorted(f["facility_types"]))
            if isinstance(val, (int, float)):
                return val
            return str(val or "")

        return sorted(facilities, key=sort_key, reverse=reverse)