import reflex as rx
from app.states.scenario_state import ScenarioState


def export_button() -> rx.Component:
    return rx.el.div(
        rx.el.h4("Export Data", class_name="font-semibold text-md"),
        rx.el.p(
            "Download current network data as CSV files.",
            class_name="text-sm text-gray-600 mt-1",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("cloud_download", class_name="mr-2"),
                "Export Facilities",
                on_click=ScenarioState.export_facilities,
                class_name="w-full flex items-center justify-center p-2 text-sm border rounded-md hover:bg-gray-100",
            ),
            rx.el.button(
                rx.icon("cloud_download", class_name="mr-2"),
                "Export Demand",
                on_click=ScenarioState.export_demand,
                class_name="w-full flex items-center justify-center p-2 text-sm border rounded-md hover:bg-gray-100",
            ),
            rx.el.button(
                rx.icon("cloud_download", class_name="mr-2"),
                "Export Sim Results",
                on_click=ScenarioState.export_simulation_results,
                class_name="w-full flex items-center justify-center p-2 text-sm border rounded-md hover:bg-gray-100",
            ),
            class_name="grid grid-cols-1 gap-2 mt-4",
        ),
        class_name="p-4",
    )