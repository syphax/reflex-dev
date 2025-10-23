import reflex as rx
import uuid
from typing import TypedDict
import datetime
import pandas as pd
import io
import logging
from app.states.map_state import Facility
from app.states.demand_state import Demand
from app.states.network_config_state import NetworkConfigState
from app.states.simulation_state import SimulationResult


class Scenario(TypedDict):
    scenario_id: str
    name: str
    timestamp: str
    facilities: list[Facility]
    demands: list[Demand]
    network_config: dict[str, list[dict] | dict]
    simulation_result: SimulationResult | None


class ScenarioState(rx.State):
    scenarios: list[Scenario] = []
    new_scenario_name: str = ""

    @rx.event
    async def save_current_scenario(self):
        if not self.new_scenario_name:
            return rx.toast.error("Scenario name cannot be empty.")
        from app.states.map_state import MapState
        from app.states.demand_state import DemandState
        from app.states.simulation_state import SimulationState

        map_state = await self.get_state(MapState)
        demand_state = await self.get_state(DemandState)
        network_config_state = await self.get_state(NetworkConfigState)
        simulation_state = await self.get_state(SimulationState)
        new_scenario = Scenario(
            scenario_id=str(uuid.uuid4()),
            name=self.new_scenario_name,
            timestamp=datetime.datetime.now().isoformat(),
            facilities=map_state.facilities,
            demands=demand_state.demands,
            network_config={
                "transport_costs": network_config_state.transport_costs,
                "truck_capacity": network_config_state.truck_capacity,
            },
            simulation_result=simulation_state.simulation_result,
        )
        self.scenarios.append(new_scenario)
        self.new_scenario_name = ""
        return rx.toast.success(f"Scenario '{new_scenario['name']}' saved.")

    @rx.event
    def remove_scenario(self, scenario_id: str):
        self.scenarios = [s for s in self.scenarios if s["scenario_id"] != scenario_id]
        return rx.toast.info("Scenario removed.")

    def _create_csv(self, data: list[dict], filename: str) -> rx.download:
        if not data:
            return rx.toast.error("No data to export.")
        df = pd.DataFrame(data)
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        return rx.download(
            data=csv_buffer.getvalue().encode(),
            filename=f"{filename}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.csv",
        )

    @rx.event
    async def export_facilities(self):
        from app.states.map_state import MapState

        map_state = await self.get_state(MapState)
        return self._create_csv(map_state.facilities, "facilities_export")

    @rx.event
    async def export_demand(self):
        from app.states.demand_state import DemandState

        demand_state = await self.get_state(DemandState)
        return self._create_csv(demand_state.demands, "demand_export")

    @rx.event
    async def export_simulation_results(self):
        from app.states.simulation_state import SimulationState

        sim_state = await self.get_state(SimulationState)
        if not sim_state.simulation_result:
            return rx.toast.error("No simulation results to export.")
        flat_results = []
        res = sim_state.simulation_result
        base_data = {
            "total_cost": res["total_cost"],
            "avg_inbound_dist": res["avg_inbound_dist"],
            "avg_outbound_dist": res["avg_outbound_dist"],
            "total_demand_units": res["total_demand_units"],
            "inbound_cost": res["cost_breakdown"].get("inbound"),
            "outbound_cost": res["cost_breakdown"].get("outbound"),
            "service_level_lt_24h_pct": res["service_levels"].get("<24h"),
            "service_level_lt_48h_pct": res["service_levels"].get("<48h"),
            "service_level_gte_48h_pct": res["service_levels"].get(">=48h"),
        }
        for facility_id, utilization in res["facility_utilization"].items():
            row = base_data.copy()
            row["facility_id"] = facility_id
            row["units_served"] = utilization
            flat_results.append(row)
        if not flat_results:
            flat_results.append(base_data)
        return self._create_csv(flat_results, "simulation_results_export")