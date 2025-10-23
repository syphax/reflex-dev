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
        zip3_population = {
            "100": 1586598,
            "900": 2899736,
            "606": 2695598,
            "770": 2296224,
            "752": 1345047,
            "331": 1250000,
            "850": 1660272,
            "921": 1425976,
            "112": 2559903,
            "787": 1028225,
            "941": 884363,
            "891": 1346769,
            "303": 1200000,
            "200": 689545,
            "021": 710000,
            "981": 737015,
            "802": 715522,
            "322": 957755,
            "926": 1200000,
            "917": 1000000,
            "913": 950000,
            "774": 900000,
            "925": 850000,
            "951": 800000,
            "330": 750000,
            "300": 700000,
            "928": 650000,
            "910": 600000,
            "117": 1500000,
            "920": 700000,
            "956": 650000,
            "958": 600000,
            "945": 1150000,
            "334": 600000,
            "328": 550000,
            "336": 500000,
            "852": 1100000,
            "853": 800000,
            "857": 542629,
            "856": 200000,
            "902": 600000,
            "906": 550000,
            "907": 500000,
            "908": 467300,
            "604": 700000,
            "605": 650000,
            "113": 1000000,
            "114": 800000,
            "104": 1472654,
            "070": 700000,
            "073": 292449,
            "080": 650000,
            "087": 600000,
            "077": 643615,
            "191": 1603797,
            "190": 600000,
            "220": 550000,
            "221": 500000,
            "201": 450000,
            "208": 400000,
            "212": 350000,
            "210": 300000,
            "481": 700000,
            "482": 639111,
            "441": 600000,
            "452": 550000,
            "432": 500000,
            "430": 450000,
            "750": 1000000,
            "761": 909585,
            "782": 1434625,
            "786": 300000,
            "785": 177934,
            "780": 250000,
            "799": 678815,
            "800": 300000,
            "801": 250000,
            "803": 200000,
            "804": 150000,
            "805": 450000,
            "806": 200000,
            "810": 150000,
            "812": 100000,
            "813": 400000,
            "815": 350000,
            "816": 300000,
            "335": 450000,
            "337": 400000,
            "338": 350000,
            "339": 300000,
            "342": 250000,
            "344": 200000,
            "346": 150000,
            "347": 100000,
            "321": 500000,
            "329": 450000,
            "327": 400000,
            "301": 400000,
            "302": 350000,
            "305": 300000,
            "306": 250000,
            "308": 200000,
            "309": 150000,
        }
        new_demands = []
        for zip3, pop in zip3_population.items():
            units = -(-pop // 1000)
            new_demands.append(
                Demand(
                    demand_id=str(uuid.uuid4()),
                    zip_code=zip3,
                    product_id="",
                    units_demanded=units,
                    assigned_facility_id="",
                )
            )
        demand_state.demands = new_demands
        return rx.toast.success("Loaded default ZIP3 demand data.")