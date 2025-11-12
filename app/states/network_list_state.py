import reflex as rx
import json
import datetime
import logging
from typing import TypedDict
from sqlmodel import text


class NetworkInfo(TypedDict):
    id: int
    network_name: str
    description: str
    created_at: str
    updated_at: str


class NetworkListState(rx.State):
    networks: list[NetworkInfo] = []

    @rx.event
    async def on_load(self):
        from app.states.auth_state import AuthState

        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated or auth_state.user_id is None:
            return rx.redirect("/login")
        try:
            async with rx.asession() as session:
                result = await session.exec(
                    text(
                        "SELECT id, network_name, description, created_at, updated_at FROM network WHERE owner_user_id = :user_id ORDER BY updated_at DESC"
                    ),
                    {"user_id": auth_state.user_id},
                )
                rows = result.all()
                self.networks = [
                    NetworkInfo(
                        id=row.id,
                        network_name=row.network_name,
                        description=row.description,
                        created_at=row.created_at.strftime("%b %d, %Y"),
                        updated_at=row.updated_at.strftime("%b %d, %Y"),
                    )
                    for row in rows
                ]
        except Exception as e:
            logging.exception(f"Failed to fetch networks: {e}")
            return rx.toast.error("Failed to load your networks.")

    @rx.event
    async def load_network(self, network_id: int):
        from app.states.map_state import MapState
        from app.states.demand_set_state import DemandSetState
        from app.states.product_state import ProductState
        from app.states.network_config_state import NetworkConfigState
        from app.states.scenario_state import ScenarioState
        from app.states.network_state import NetworkState

        try:
            async with rx.asession() as session:
                network_meta_result = await session.exec(
                    text("SELECT network_name FROM network WHERE id = :network_id"),
                    {"network_id": network_id},
                )
                network_meta = network_meta_result.first()
                if not network_meta:
                    yield rx.toast.error("Network not found.")
                    return
                data_result_res = await session.exec(
                    text(
                        "SELECT facilities_json, demand_sets_json, products_json, config_json, scenarios_json FROM network_data WHERE network_id = :network_id"
                    ),
                    {"network_id": network_id},
                )
                data_result = data_result_res.first()
                if not data_result:
                    yield rx.toast.error("Network data not found.")
                    return
            map_state = await self.get_state(MapState)
            demand_set_state = await self.get_state(DemandSetState)
            product_state = await self.get_state(ProductState)
            network_config_state = await self.get_state(NetworkConfigState)
            scenario_state = await self.get_state(ScenarioState)
            network_state = await self.get_state(NetworkState)
            map_state.facilities = json.loads(data_result.facilities_json)
            demand_set_state.demand_sets = json.loads(data_result.demand_sets_json)
            product_state.products = json.loads(data_result.products_json)
            scenarios_json = json.loads(data_result.scenarios_json)
            config_json = json.loads(data_result.config_json)
            scenario_state.scenarios = scenarios_json
            network_config_state.transport_costs = config_json.get(
                "transport_costs", []
            )
            network_config_state.truck_capacity = config_json.get("truck_capacity", {})
            network_config_state.inbound_sources = config_json.get(
                "inbound_sources", []
            )
            network_config_state.edge_overrides = config_json.get("edge_overrides", [])
            network_state.current_network_id = network_id
            network_state.current_network_name = network_meta.network_name
            yield rx.redirect("/")
            yield rx.toast.success(f"Loaded network: {network_meta.network_name}")
            return
        except Exception as e:
            logging.exception(f"Failed to load network: {e}")
            yield rx.toast.error("An error occurred while loading the network.")
            return