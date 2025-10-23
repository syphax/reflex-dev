import reflex as rx
from app.states.network_config_state import (
    NetworkConfigState,
    TransportCost,
    InboundSource,
)


def network_config_editor() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Network Configuration", class_name="font-semibold text-lg px-4 pt-4"),
        transport_cost_settings(),
        truck_capacity_settings(),
        inbound_sources_list(),
        class_name="flex-1 overflow-y-auto divide-y",
    )


def transport_cost_settings() -> rx.Component:
    return rx.el.div(
        rx.el.h4("Transport Costs", class_name="font-semibold text-md mb-2"),
        rx.foreach(NetworkConfigState.transport_costs, transport_cost_row),
        class_name="p-4",
    )


def transport_cost_row(cost: TransportCost) -> rx.Component:
    return rx.el.div(
        rx.el.label(f"{cost['mode']} Cost ($/mile)", class_name="text-sm font-medium"),
        rx.el.input(
            default_value=cost["cost_per_mile"].to_string(),
            on_blur=lambda val: NetworkConfigState.update_transport_cost(
                cost["mode"], val
            ),
            class_name="w-full p-1 border rounded-md text-sm",
        ),
        class_name="grid grid-cols-2 items-center gap-4 mb-2",
    )


def truck_capacity_settings() -> rx.Component:
    return rx.el.div(
        rx.el.h4("Truck Capacity", class_name="font-semibold text-md mb-2"),
        rx.el.div(
            rx.el.label("Max Volume (cu ft)", class_name="text-sm font-medium"),
            rx.el.input(
                default_value=NetworkConfigState.truck_capacity[
                    "max_volume_cuft"
                ].to_string(),
                on_blur=lambda val: NetworkConfigState.update_truck_capacity(
                    "max_volume_cuft", val
                ),
                class_name="w-full p-1 border rounded-md text-sm",
            ),
            class_name="grid grid-cols-2 items-center gap-4 mb-2",
        ),
        rx.el.div(
            rx.el.label("Max Weight (lbs)", class_name="text-sm font-medium"),
            rx.el.input(
                default_value=NetworkConfigState.truck_capacity[
                    "max_weight_lbs"
                ].to_string(),
                on_blur=lambda val: NetworkConfigState.update_truck_capacity(
                    "max_weight_lbs", val
                ),
                class_name="w-full p-1 border rounded-md text-sm",
            ),
            class_name="grid grid-cols-2 items-center gap-4",
        ),
        class_name="p-4",
    )


def inbound_sources_list() -> rx.Component:
    return rx.el.div(
        rx.el.h4(
            "Inbound Sources (Top 25 US Ports)", class_name="font-semibold text-md mb-2"
        ),
        rx.el.div(
            rx.foreach(NetworkConfigState.inbound_sources, inbound_source_item),
            class_name="space-y-1 text-sm",
        ),
        class_name="p-4",
    )


def inbound_source_item(source: InboundSource) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("anchor", class_name="w-4 h-4 text-gray-500"),
            rx.el.span(source["name"], class_name="font-medium"),
            class_name="flex items-center gap-2",
        ),
        rx.el.span(source["location"], class_name="text-gray-600"),
        class_name="flex items-center justify-between p-1.5 rounded hover:bg-gray-100",
    )