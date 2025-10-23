import reflex as rx
from typing import TypedDict, Any
import math
import logging
import itertools
from app.states.map_state import MapState, Facility
from app.states.demand_state import DemandState
from app.states.network_config_state import NetworkConfigState


class SimulationResult(TypedDict):
    total_cost: float
    cost_breakdown: dict[str, float]
    service_levels: dict[str, float]
    facility_utilization: dict[str, int]
    avg_inbound_dist: float
    avg_outbound_dist: float
    total_demand_units: int


class OptimizationResult(TypedDict):
    optimal_facilities: list[str]
    best_cost: float
    baseline_cost: float
    cost_savings: float


class SimulationState(rx.State):
    is_simulating: bool = False
    simulation_progress: float = 0.0
    simulation_result: SimulationResult | None = None
    error_message: str = ""
    is_optimizing: bool = False
    optimization_progress: float = 0.0
    optimization_result: OptimizationResult | None = None
    num_dcs_to_select: int = 5
    candidate_facility_type: str = "DC"

    def _haversine_distance(
        self, lat1: float, lon1: float, lat2: float, lon2: float
    ) -> float:
        R = 3958.8
        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        lat1 = math.radians(lat1)
        lat2 = math.radians(lat2)
        a = (
            math.sin(dLat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(dLon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    async def _calculate_cost_for_facilities(self, facilities: list[Facility]):
        demand_state = await self.get_state(DemandState)
        network_config_state = await self.get_state(NetworkConfigState)
        demands = demand_state.demands
        transport_costs = network_config_state.transport_costs
        total_cost = 0.0
        cost_breakdown = {"inbound": 0.0, "outbound": 0.0}
        service_levels = {"<24h": 0, "<48h": 0, ">=48h": 0}
        facility_utilization = {f["facility_id"]: 0 for f in facilities}
        total_inbound_dist, total_outbound_dist = (0, 0)
        total_demand_units = sum((d["units_demanded"] for d in demands)) or 1
        la_port_lat, la_port_lon = (33.7292, -118.262)
        tl_cost = next(
            (c["cost_per_mile"] for c in transport_costs if c["mode"] == "TL"), 3.0
        )
        parcel_cost = next(
            (c["cost_per_mile"] for c in transport_costs if c["mode"] == "Parcel"), 0.5
        )
        for demand in demands:
            facility = next(
                (
                    f
                    for f in facilities
                    if f["facility_id"] == demand["assigned_facility_id"]
                ),
                None,
            )
            if not facility:
                continue
            inbound_dist = self._haversine_distance(
                la_port_lat, la_port_lon, facility["latitude"], facility["longitude"]
            )
            inbound_cost = inbound_dist * tl_cost * demand["units_demanded"]
            total_cost += inbound_cost
            cost_breakdown["inbound"] += inbound_cost
            total_inbound_dist += inbound_dist * demand["units_demanded"]
            outbound_dist = 50
            outbound_cost = outbound_dist * parcel_cost * demand["units_demanded"]
            total_cost += outbound_cost
            cost_breakdown["outbound"] += outbound_cost
            total_outbound_dist += outbound_dist * demand["units_demanded"]
            if outbound_dist <= 500:
                service_levels["<24h"] += demand["units_demanded"]
            elif 500 < outbound_dist <= 1000:
                service_levels["<48h"] += demand["units_demanded"]
            else:
                service_levels[">=48h"] += demand["units_demanded"]
            facility_utilization[facility["facility_id"]] += demand["units_demanded"]
        service_level_pct = {
            k: v / total_demand_units * 100 for k, v in service_levels.items()
        }
        return {
            "total_cost": total_cost,
            "cost_breakdown": cost_breakdown,
            "service_levels": service_level_pct,
            "facility_utilization": facility_utilization,
            "avg_inbound_dist": total_inbound_dist / total_demand_units,
            "avg_outbound_dist": total_outbound_dist / total_demand_units,
            "total_demand_units": total_demand_units,
        }

    @rx.event(background=True)
    async def run_simulation(self):
        async with self:
            self.is_simulating = True
            self.simulation_progress = 0
            self.simulation_result = None
            self.error_message = ""
        try:
            async with self:
                map_state = await self.get_state(MapState)
                facilities = map_state.facilities
                demand_state = await self.get_state(DemandState)
                if not facilities or not demand_state.demands:
                    self.error_message = "No facilities or demand points to simulate."
                    self.is_simulating = False
                    return
                self.simulation_progress = 50
            result = await self._calculate_cost_for_facilities(facilities)
            async with self:
                self.simulation_result = result
                self.simulation_progress = 100
        except Exception as e:
            logging.exception(f"Simulation failed: {e}")
            async with self:
                self.error_message = f"An error occurred: {e}"
        finally:
            async with self:
                self.is_simulating = False

    @rx.event(background=True)
    async def run_optimization(self):
        async with self:
            self.is_optimizing = True
            self.optimization_progress = 0
            self.optimization_result = None
            self.error_message = ""
        try:
            async with self:
                map_state = await self.get_state(MapState)
                all_facilities = map_state.facilities
            candidate_facilities = [
                f
                for f in all_facilities
                if f["facility_type"] == self.candidate_facility_type
            ]
            if len(candidate_facilities) < self.num_dcs_to_select:
                async with self:
                    self.error_message = (
                        "Not enough candidate facilities to run optimization."
                    )
                    self.is_optimizing = False
                return
            baseline_result = await self._calculate_cost_for_facilities(all_facilities)
            baseline_cost = baseline_result["total_cost"]
            best_cost = float("inf")
            best_combination = None
            combinations = list(
                itertools.combinations(candidate_facilities, self.num_dcs_to_select)
            )
            for i, combo in enumerate(combinations):
                current_network = [
                    f
                    for f in all_facilities
                    if f["facility_type"] != self.candidate_facility_type
                ] + list(combo)
                result = await self._calculate_cost_for_facilities(current_network)
                if result["total_cost"] < best_cost:
                    best_cost = result["total_cost"]
                    best_combination = [f["site_name"] for f in combo]
                async with self:
                    self.optimization_progress = (i + 1) / len(combinations) * 100
                yield
            if best_combination:
                async with self:
                    self.optimization_result = {
                        "optimal_facilities": best_combination,
                        "best_cost": best_cost,
                        "baseline_cost": baseline_cost,
                        "cost_savings": baseline_cost - best_cost,
                    }
        except Exception as e:
            logging.exception(f"Optimization failed: {e}")
            async with self:
                self.error_message = f"An error occurred during optimization: {e}"
        finally:
            async with self:
                self.is_optimizing = False

    @rx.var
    def sorted_facility_utilization(self) -> list[tuple[str, int]]:
        if (
            not self.simulation_result
            or not self.simulation_result["facility_utilization"]
        ):
            return []
        return sorted(
            self.simulation_result["facility_utilization"].items(),
            key=lambda item: item[1],
            reverse=True,
        )[:5]