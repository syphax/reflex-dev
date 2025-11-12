import reflex as rx
from app.states.network_list_state import NetworkListState, NetworkInfo
from app.components.sidebar import header


def network_card(network: NetworkInfo) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(network["network_name"], class_name="text-lg font-bold"),
            rx.el.p(
                rx.cond(
                    network["description"],
                    network["description"],
                    "No description provided.",
                ),
                class_name="mt-2 text-sm text-gray-600 flex-grow",
            ),
            class_name="flex flex-col h-full",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    f"Last updated: {network['updated_at']}",
                    class_name="text-xs text-gray-500",
                ),
                class_name="mt-4",
            ),
            rx.el.button(
                "Load Network",
                on_click=lambda: NetworkListState.load_network(network["id"]),
                class_name="w-full mt-4 bg-violet-600 text-white p-2 rounded-md hover:bg-violet-700 text-sm font-semibold",
            ),
        ),
        class_name="bg-white p-6 rounded-lg shadow-md border flex flex-col justify-between",
    )


def my_networks_page() -> rx.Component:
    return rx.el.div(
        header(),
        rx.el.div(
            rx.el.a(
                rx.icon("arrow-left", class_name="w-5 h-5 mr-2"),
                "Back to Map",
                href="/",
                class_name="flex items-center text-violet-600 hover:underline mb-6 text-sm font-medium",
            ),
            rx.el.h1("My Networks", class_name="text-3xl font-bold mb-6"),
            rx.cond(
                NetworkListState.networks.length() > 0,
                rx.el.div(
                    rx.foreach(NetworkListState.networks, network_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                ),
                rx.el.div(
                    rx.icon("folder-x", class_name="w-16 h-16 text-gray-400"),
                    rx.el.h3(
                        "No Networks Found", class_name="mt-4 text-xl font-semibold"
                    ),
                    rx.el.p(
                        "You haven't saved any networks yet.",
                        class_name="mt-2 text-gray-500",
                    ),
                    rx.el.a(
                        "Create your first network",
                        href="/",
                        class_name="mt-4 text-violet-600 font-semibold hover:underline",
                    ),
                    class_name="text-center col-span-full py-24",
                ),
            ),
            class_name="container mx-auto p-8",
        ),
        on_mount=NetworkListState.on_load,
        class_name="bg-gray-50 min-h-screen font-['Inter']",
    )