import reflex as rx
import uuid
import logging
from typing import TypedDict
from app.states.demand_state import DemandState, Demand


class DemandSet(TypedDict):
    name: str
    demands: list[Demand]


class DemandSetState(rx.State):
    demand_sets: list[DemandSet] = []
    current_demand_set_name: str = ""
    new_demand_set_name: str = ""

    @rx.var
    def demand_set_names(self) -> list[str]:
        return [ds["name"] for ds in self.demand_sets]

    @rx.event
    async def save_current_demand_set(self):
        if not self.current_demand_set_name:
            return rx.toast.error("No demand set selected to save.")
        demand_state = await self.get_state(DemandState)
        for i, ds in enumerate(self.demand_sets):
            if ds["name"] == self.current_demand_set_name:
                self.demand_sets[i]["demands"] = demand_state.demands
                return rx.toast.success(
                    f"Demand set '{self.current_demand_set_name}' saved."
                )

    @rx.event
    def delete_current_demand_set(self):
        if not self.current_demand_set_name:
            return rx.toast.error("No demand set selected to delete.")
        self.demand_sets = [
            ds for ds in self.demand_sets if ds["name"] != self.current_demand_set_name
        ]
        self.current_demand_set_name = ""
        return rx.toast.info("Demand set deleted.")

    @rx.event
    async def create_new_demand_set(self):
        if not self.new_demand_set_name:
            return rx.toast.error("New demand set name cannot be empty.")
        if any((ds["name"] == self.new_demand_set_name for ds in self.demand_sets)):
            return rx.toast.error("A demand set with this name already exists.")
        demand_state = await self.get_state(DemandState)
        new_set = DemandSet(
            name=self.new_demand_set_name, demands=list(demand_state.demands)
        )
        self.demand_sets.append(new_set)
        self.current_demand_set_name = self.new_demand_set_name
        self.new_demand_set_name = ""
        return rx.toast.success(f"Demand set '{new_set['name']}' created.")

    @rx.event
    async def load_default_zip3_demand(self):
        demand_state = await self.get_state(DemandState)
        demand_state.demands = [
            Demand(
                demand_id=str(uuid.uuid4()),
                zip_code="90210",
                product_id="",
                units_demanded=150,
                assigned_facility_id="",
            ),
            Demand(
                demand_id=str(uuid.uuid4()),
                zip_code="10001",
                product_id="",
                units_demanded=200,
                assigned_facility_id="",
            ),
        ]
        return rx.toast.success("Loaded default ZIP3 demand data.")