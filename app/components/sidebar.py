import reflex as rx
from app.states.map_state import MapState, FACILITY_COLORS, FacilityType
from app.states.auth_state import AuthState
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


from app.states.network_state import NetworkState


def save_network_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(
            rx.el.button(
                rx.icon("save", class_name="w-4 h-4 mr-2"),
                "Save Network",
                class_name="bg-violet-600 text-white px-3 py-1 rounded-md text-sm hover:bg-violet-700 flex items-center",
            )
        ),
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title("Save Network"),
            rx.radix.primitives.dialog.description(
                "Save the current network configuration to your account."
            ),
            rx.el.div(
                rx.el.label(
                    "Network Name", class_name="text-sm font-medium text-gray-700"
                ),
                rx.el.input(
                    placeholder="My Awesome Network",
                    on_change=NetworkState.set_new_network_name,
                    default_value=NetworkState.new_network_name,
                    class_name="w-full p-2 border rounded-md text-sm mt-1",
                ),
                class_name="mt-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Description (Optional)",
                    class_name="text-sm font-medium text-gray-700",
                ),
                rx.el.textarea(
                    placeholder="A brief description of this network...",
                    on_change=NetworkState.set_new_network_description,
                    default_value=NetworkState.new_network_description,
                    class_name="w-full p-2 border rounded-md text-sm mt-1",
                ),
                class_name="mt-4",
            ),
            rx.el.div(
                rx.radix.primitives.dialog.close(
                    rx.el.button(
                        "Cancel",
                        class_name="bg-gray-200 text-gray-700 px-4 py-2 rounded-md text-sm hover:bg-gray-300",
                    )
                ),
                rx.el.button(
                    "Save",
                    on_click=NetworkState.save_network,
                    class_name="bg-violet-600 text-white px-4 py-2 rounded-md text-sm hover:bg-violet-700",
                ),
                class_name="flex justify-end gap-3 mt-4",
            ),
        ),
    )


def header() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(tag="network", class_name="h-8 w-8 text-violet-600"),
            rx.el.div(
                rx.el.h2("Network Design", class_name="text-xl font-bold"),
                rx.cond(
                    NetworkState.current_network_name,
                    rx.el.span(
                        f"Editing: {NetworkState.current_network_name}",
                        class_name="text-xs text-gray-500 bg-gray-100 px-2 py-0.5 rounded-full",
                    ),
                ),
            ),
            class_name="flex items-center gap-2",
        ),
        rx.el.div(
            rx.el.a(
                rx.el.button(
                    rx.icon("folder-search", class_name="w-4 h-4 mr-2"),
                    "My Networks",
                    class_name="bg-gray-200 text-gray-700 px-3 py-1 rounded-md text-sm hover:bg-gray-300 flex items-center",
                ),
                href="/my-networks",
            ),
            save_network_dialog(),
            rx.el.div(
                rx.cond(
                    AuthState.is_authenticated,
                    rx.cond(
                        AuthState.show_user_menu,
                        rx.el.div(
                            rx.el.div(
                                rx.el.p(
                                    AuthState.user_info.username,
                                    class_name="font-semibold",
                                ),
                                rx.el.p(
                                    AuthState.user_info.email,
                                    class_name="text-sm text-gray-500",
                                ),
                                class_name="p-2 border-b",
                            ),
                            rx.el.button(
                                "Profile",
                                on_click=rx.redirect("/profile"),
                                class_name="w-full text-left px-4 py-2 text-sm hover:bg-gray-100",
                            ),
                            rx.el.button(
                                "Log Out",
                                on_click=AuthState.logout,
                                class_name="w-full text-left px-4 py-2 text-sm text-red-500 hover:bg-red-50",
                            ),
                            class_name="absolute top-12 right-0 w-48 bg-white rounded-md shadow-lg border z-20 divide-y",
                            on_mouse_leave=lambda: AuthState.set_show_user_menu(False),
                        ),
                    ),
                ),
                rx.el.button(
                    rx.image(
                        src=f"https://api.dicebear.com/9.x/initials/svg?seed={AuthState.user_info.username}",
                        class_name="w-8 h-8 rounded-full",
                    ),
                    on_click=AuthState.toggle_user_menu,
                    class_name="relative",
                ),
                class_name="relative",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="flex items-center justify-between p-4 border-b",
    )


def sidebar() -> rx.Component:
    return rx.el.div(
        header(),
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