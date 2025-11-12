import reflex as rx
import json
import datetime
import logging
from sqlmodel import text


class NetworkState(rx.State):
    current_network_id: int | None = None
    current_network_name: str = ""
    new_network_name: str = ""
    new_network_description: str = ""

    @rx.event
    async def save_network(self):
        from app.states.auth_state import AuthState
        from app.states.map_state import MapState
        from app.states.demand_set_state import DemandSetState
        from app.states.product_state import ProductState
        from app.states.network_config_state import NetworkConfigState
        from app.states.scenario_state import ScenarioState

        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated or auth_state.user_id is None:
            return rx.toast.error("You must be logged in to save a network.")
        if not self.new_network_name:
            return rx.toast.error("Network name is required.")
        try:
            map_state = await self.get_state(MapState)
            demand_set_state = await self.get_state(DemandSetState)
            product_state = await self.get_state(ProductState)
            network_config_state = await self.get_state(NetworkConfigState)
            scenario_state = await self.get_state(ScenarioState)
            facilities_json = json.dumps(map_state.facilities)
            demand_sets_json = json.dumps(demand_set_state.demand_sets)
            products_json = json.dumps(product_state.products)
            config_json = json.dumps(
                {
                    "transport_costs": network_config_state.transport_costs,
                    "truck_capacity": network_config_state.truck_capacity,
                    "inbound_sources": network_config_state.inbound_sources,
                    "edge_overrides": network_config_state.edge_overrides,
                }
            )
            scenarios_json = json.dumps(scenario_state.scenarios)
            with rx.session() as session:
                now = datetime.datetime.now(datetime.timezone.utc)
                result = session.exec(
                    text(
                        "INSERT INTO network (owner_user_id, network_name, description, is_public, created_at, updated_at) VALUES (:owner_user_id, :network_name, :description, :is_public, :created_at, :updated_at) RETURNING id"
                    ),
                    {
                        "owner_user_id": auth_state.user_id,
                        "network_name": self.new_network_name,
                        "description": self.new_network_description,
                        "is_public": False,
                        "created_at": now,
                        "updated_at": now,
                    },
                ).first()
                if not result or not result[0]:
                    raise Exception("Failed to create network record.")
                network_id = result[0]
                session.exec(
                    text(
                        "INSERT INTO network_data (network_id, facilities_json, demand_sets_json, products_json, config_json, scenarios_json) VALUES (:network_id, :facilities_json, :demand_sets_json, :products_json, :config_json, :scenarios_json)"
                    ),
                    {
                        "network_id": network_id,
                        "facilities_json": facilities_json,
                        "demand_sets_json": demand_sets_json,
                        "products_json": products_json,
                        "config_json": config_json,
                        "scenarios_json": scenarios_json,
                    },
                )
                session.commit()
                self.current_network_id = network_id
                self.current_network_name = self.new_network_name
                self.new_network_name = ""
                self.new_network_description = ""
            return rx.toast.success(f"Network '{self.current_network_name}' saved!")
        except Exception as e:
            logging.exception(f"Failed to save network: {e}")
            return rx.toast.error("An unexpected error occurred while saving.")

    @rx.event
    def clear_current_network(self):
        self.current_network_id = None
        self.current_network_name = ""