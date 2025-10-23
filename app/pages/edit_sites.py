import reflex as rx
from app.states.edit_sites_state import EditSitesState
from app.states.map_state import Facility


def sortable_header(label: str, column_key: str) -> rx.Component:
    return rx.el.th(
        rx.el.button(
            label,
            rx.icon(
                tag=rx.cond(
                    EditSitesState.sort_order == "asc", "arrow-up", "arrow-down"
                ),
                class_name=rx.cond(
                    EditSitesState.sort_by == column_key, "w-4 h-4 ml-2", "hidden"
                ),
            ),
            on_click=lambda: EditSitesState.set_sort_column(column_key),
            class_name="flex items-center font-medium text-gray-600 hover:text-gray-900",
        ),
        scope="col",
        class_name="px-4 py-3 text-left text-sm",
    )


def facility_table_row(facility: Facility) -> rx.Component:
    return rx.el.tr(
        rx.el.td(facility["site_name"], class_name="px-4 py-3 whitespace-nowrap"),
        rx.el.td(facility["facility_type"], class_name="px-4 py-3 whitespace-nowrap"),
        rx.el.td(facility["parent_company"], class_name="px-4 py-3 whitespace-nowrap"),
        rx.el.td(facility["street_address"], class_name="px-4 py-3 whitespace-nowrap"),
        rx.el.td(facility["city"], class_name="px-4 py-3 whitespace-nowrap"),
        rx.el.td(facility["state_province"], class_name="px-4 py-3 whitespace-nowrap"),
        rx.el.td(facility["zip5"], class_name="px-4 py-3 whitespace-nowrap"),
        rx.el.td(
            f"{facility['latitude']:.4f}, {facility['longitude']:.4f}",
            class_name="px-4 py-3 whitespace-nowrap",
        ),
        class_name="border-b hover:bg-gray-50 text-sm",
    )


def edit_sites_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.a(
                rx.icon("arrow-left", class_name="w-5 h-5 mr-2"),
                "Back to Map",
                href="/",
                class_name="flex items-center text-violet-600 hover:underline mb-4",
            ),
            rx.el.h1("Edit Facilities", class_name="text-3xl font-bold mb-4"),
            rx.el.input(
                placeholder="Search facilities...",
                on_change=EditSitesState.set_search_query.debounce(300),
                class_name="w-full max-w-md px-4 py-2 border rounded-lg mb-6",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            sortable_header("Site Name", "site_name"),
                            sortable_header("Type", "facility_type"),
                            sortable_header("Parent Company", "parent_company"),
                            sortable_header("Address", "street_address"),
                            sortable_header("City", "city"),
                            sortable_header("State", "state_province"),
                            sortable_header("ZIP", "zip5"),
                            sortable_header("Coordinates", "latitude"),
                            class_name="bg-gray-50 border-b",
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            EditSitesState.filtered_and_sorted_facilities,
                            facility_table_row,
                        ),
                        class_name="bg-white divide-y divide-gray-200",
                    ),
                    class_name="min-w-full",
                ),
                class_name="border rounded-lg overflow-x-auto shadow-sm",
            ),
            class_name="container mx-auto p-8",
        ),
        on_mount=EditSitesState.on_load,
        class_name="bg-gray-100 min-h-screen font-['Inter']",
    )