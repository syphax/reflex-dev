import reflex as rx
import uuid
from typing import Literal, TypedDict
import logging
from app.states.map_state import Facility
from app.states.product_state import Product


class Demand(TypedDict):
    demand_id: str
    zip_code: str
    product_id: str
    units_demanded: int
    assigned_facility_id: str


class DemandState(rx.State):
    demands: list[Demand] = []
    selected_product_id: str = ""
    selected_facility_id: str = ""

    @rx.event
    def handle_submit(self, form_data: dict):
        zip_code = form_data.get("zip_code", "")
        units_demanded_str = form_data.get("units_demanded", "100")
        if (
            not zip_code
            or not self.selected_product_id
            or (not self.selected_facility_id)
        ):
            return rx.toast.error("ZIP, product, and facility must be selected.")
        try:
            units_demanded = int(units_demanded_str)
        except ValueError as e:
            logging.exception(f"Error: {e}")
            return rx.toast.error("Invalid number for units demanded.")
        new_demand = Demand(
            demand_id=str(uuid.uuid4()),
            zip_code=zip_code,
            product_id=self.selected_product_id,
            units_demanded=units_demanded,
            assigned_facility_id=self.selected_facility_id,
        )
        self.demands.append(new_demand)

    @rx.event
    def remove_demand(self, demand_id: str):
        self.demands = [d for d in self.demands if d["demand_id"] != demand_id]