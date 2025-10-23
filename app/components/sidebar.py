import reflex as rx
from app.states.map_state import MapState, FACILITY_COLORS, FacilityType
from app.components.file_upload_component import file_upload_component
from app.components.product_editor import product_attributes_editor
from app.components.demand_editor import demand_editor
from app.components.network_config_editor import network_config_editor
from app.components.simulation_panel import simulation_panel
from app.components.scenario_view import scenario_view


class SidebarState(rx.State):
    active_tab: str = "Facilities"
    is_resized: bool = False

    @rx.event
    def toggle_resize(self):
        self.is_resized = not self.is_resized


def facility_type_selector() -> rx.Component:
    return rx.el.div(
        rx.el.label("Facility Type", class_name="font-semibold text-gray-700"),
        rx.el.select(
            rx.foreach(
                list(FACILITY_COLORS.keys()),
                lambda type: rx.el.option(type, value=type),
            ),
            value=MapState.selected_facility_type,
            on_change=MapState.set_selected_facility_type,
            class_name="w-full p-2 border rounded-md bg-white",
        ),
        class_name="p-4 border-b",
    )


def facility_list_item(facility: dict) -> rx.Component:
    colors_var = rx.Var.create(FACILITY_COLORS)
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                class_name="h-4 w-4 rounded-full border",
                style={"background_color": colors_var[facility["facility_type"]]},
            ),
            rx.el.span(facility["site_name"], class_name="font-medium"),
            class_name="flex items-center gap-3 flex-1",
        ),
        rx.el.button(
            rx.icon(tag=rx.cond(facility["is_active"], "eye", "eye-off"), size=18),
            on_click=lambda: MapState.toggle_facility_active(facility["facility_id"]),
            class_name="p-1 text-gray-500 hover:text-gray-800",
        ),
        rx.el.button(
            rx.icon(tag="trash-2", size=18),
            on_click=lambda: MapState.remove_facility(facility["facility_id"]),
            class_name="p-1 text-red-500 hover:text-red-700",
        ),
        class_name="flex items-center justify-between p-2 rounded-md hover:bg-gray-100",
    )


def facility_list() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Facilities", class_name="font-semibold text-lg"),
            rx.el.a(
                rx.el.button(
                    "Edit Sites",
                    rx.icon("copy", class_name="w-4 h-4 ml-2"),
                    class_name="bg-gray-200 text-gray-700 px-3 py-1 rounded-md text-sm hover:bg-gray-300 flex items-center",
                ),
                href="/edit-sites",
            ),
            class_name="flex justify-between items-center px-4 pt-4",
        ),
        rx.el.div(
            rx.foreach(MapState.facilities, facility_list_item),
            class_name="flex flex-col p-2",
        ),
        class_name="flex-1 overflow-y-auto",
    )


def facilities_tab_content() -> rx.Component:
    return rx.el.div(
        facility_type_selector(),
        file_upload_component(),
        facility_list(),
        class_name="flex flex-col h-full",
    )


def sidebar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(tag="network", class_name="h-8 w-8 text-violet-600"),
            rx.el.h2("Network Design", class_name="text-xl font-bold"),
            class_name="flex items-center gap-2 p-4 border-b",
        ),
        rx.el.div(
            rx.el.button(
                "Facilities",
                on_click=lambda: SidebarState.set_active_tab("Facilities"),
                class_name=rx.cond(
                    SidebarState.active_tab == "Facilities",
                    "border-b-2 border-violet-600 text-violet-600 font-semibold",
                    "text-gray-500 hover:text-gray-700",
                ),
                style={"padding": "1rem", "flex": 1, "backgroundColor": "transparent"},
            ),
            rx.el.button(
                "Products",
                on_click=lambda: SidebarState.set_active_tab("Products"),
                class_name=rx.cond(
                    SidebarState.active_tab == "Products",
                    "border-b-2 border-violet-600 text-violet-600 font-semibold",
                    "text-gray-500 hover:text-gray-700",
                ),
                style={"padding": "1rem", "flex": 1, "backgroundColor": "transparent"},
            ),
            rx.el.button(
                "Demand",
                on_click=lambda: SidebarState.set_active_tab("Demand"),
                class_name=rx.cond(
                    SidebarState.active_tab == "Demand",
                    "border-b-2 border-violet-600 text-violet-600 font-semibold",
                    "text-gray-500 hover:text-gray-700",
                ),
                style={"padding": "1rem", "flex": 1, "backgroundColor": "transparent"},
            ),
            rx.el.button(
                "Network Config",
                on_click=lambda: SidebarState.set_active_tab("Network Config"),
                class_name=rx.cond(
                    SidebarState.active_tab == "Network Config",
                    "border-b-2 border-violet-600 text-violet-600 font-semibold",
                    "text-gray-500 hover:text-gray-700",
                ),
                style={"padding": "1rem", "flex": 1, "backgroundColor": "transparent"},
            ),
            rx.el.button(
                "Simulation",
                on_click=lambda: SidebarState.set_active_tab("Simulation"),
                class_name=rx.cond(
                    SidebarState.active_tab == "Simulation",
                    "border-b-2 border-violet-600 text-violet-600 font-semibold",
                    "text-gray-500 hover:text-gray-700",
                ),
                style={"padding": "1rem", "flex": 1, "backgroundColor": "transparent"},
            ),
            rx.el.button(
                "Scenarios",
                on_click=lambda: SidebarState.set_active_tab("Scenarios"),
                class_name=rx.cond(
                    SidebarState.active_tab == "Scenarios",
                    "border-b-2 border-violet-600 text-violet-600 font-semibold",
                    "text-gray-500 hover:text-gray-700",
                ),
                style={"padding": "1rem", "flex": 1, "backgroundColor": "transparent"},
            ),
            class_name="flex w-full border-b",
        ),
        rx.match(
            SidebarState.active_tab,
            ("Facilities", facilities_tab_content()),
            ("Products", product_attributes_editor()),
            ("Demand", demand_editor()),
            ("Network Config", network_config_editor()),
            ("Simulation", simulation_panel()),
            ("Scenarios", scenario_view()),
            rx.el.div(),
        ),
        rx.el.div(
            rx.el.button(
                rx.icon(
                    tag=rx.cond(
                        SidebarState.is_resized, "chevrons-left", "chevrons-right"
                    )
                ),
                on_click=SidebarState.toggle_resize,
                class_name="absolute top-1/2 -right-3 transform -translate-y-1/2 bg-gray-200 hover:bg-gray-300 p-1 rounded-full z-10",
            ),
            class_name="relative",
        ),
        class_name=rx.cond(
            SidebarState.is_resized,
            "flex flex-col bg-gray-50 border-r w-[800px] h-screen transition-all duration-300",
            "flex flex-col bg-gray-50 border-r w-96 h-screen transition-all duration-300",
        ),
    )