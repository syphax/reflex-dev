import reflex as rx
from app.states.demand_state import DemandState, Demand
from app.states.map_state import MapState
from app.states.product_state import ProductState
from app.states.demand_set_state import DemandSetState


def demand_editor() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Demand", class_name="font-semibold text-lg"),
            class_name="flex justify-between items-center px-4 pt-4",
        ),
        demand_set_manager(),
        add_demand_form(),
        demand_list(),
        class_name="flex-1 overflow-y-auto",
    )


def demand_set_manager() -> rx.Component:
    return rx.el.div(
        rx.el.h4("Demand Sets", class_name="font-semibold text-md"),
        rx.el.div(
            rx.el.select(
                rx.foreach(
                    DemandSetState.demand_set_names,
                    lambda name: rx.el.option(name, value=name),
                ),
                value=DemandSetState.current_demand_set_name,
                on_change=DemandSetState.set_current_demand_set_name,
                class_name="w-full p-1.5 border rounded-md text-sm bg-white",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("save", size=16),
                    on_click=DemandSetState.save_current_demand_set,
                    class_name="p-2 border rounded-md hover:bg-gray-100",
                ),
                rx.el.button(
                    rx.icon("trash-2", size=16),
                    on_click=DemandSetState.delete_current_demand_set,
                    class_name="p-2 border rounded-md text-red-500 hover:bg-red-50",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center gap-2 mt-2",
        ),
        rx.el.div(
            rx.el.input(
                placeholder="New demand set name...",
                on_change=DemandSetState.set_new_demand_set_name,
                class_name="w-full p-1 border rounded-md text-sm",
                default_value=DemandSetState.new_demand_set_name,
            ),
            rx.el.button(
                "Create",
                on_click=DemandSetState.create_new_demand_set,
                class_name="bg-blue-500 text-white px-3 py-1.5 rounded-md hover:bg-blue-600 text-sm",
            ),
            class_name="flex items-center gap-2 mt-2",
        ),
        rx.el.button(
            "Load Default ZIP3 Demand",
            on_click=DemandSetState.load_default_zip3_demand,
            class_name="w-full bg-gray-200 p-1.5 rounded-md hover:bg-gray-300 text-sm mt-2",
        ),
        class_name="p-4 border-b bg-gray-50",
    )


def add_demand_form() -> rx.Component:
    return rx.el.form(
        rx.el.div(
            rx.el.label("ZIP Code", class_name="text-sm font-medium"),
            rx.el.input(
                placeholder="e.g., 90210",
                name="zip_code",
                class_name="w-full p-1 border rounded-md text-sm",
            ),
            class_name="col-span-1",
        ),
        rx.el.div(
            rx.el.label("Units Demanded", class_name="text-sm font-medium"),
            rx.el.input(
                placeholder="100",
                name="units_demanded",
                type="number",
                default_value="100",
                class_name="w-full p-1 border rounded-md text-sm",
            ),
            class_name="col-span-1",
        ),
        rx.el.div(
            rx.el.label("Product", class_name="text-sm font-medium"),
            rx.el.select(
                rx.el.option("Select Product", value="", disabled=True),
                rx.foreach(
                    ProductState.products,
                    lambda p: rx.el.option(p["product_name"], value=p["product_id"]),
                ),
                on_change=DemandState.set_selected_product_id,
                value=DemandState.selected_product_id,
                class_name="w-full p-1.5 border rounded-md text-sm bg-white",
            ),
            class_name="col-span-2",
        ),
        rx.el.button(
            rx.icon("plus", size=16),
            "Add Demand Point",
            type="submit",
            class_name="col-span-full bg-blue-500 text-white p-1.5 rounded-md hover:bg-blue-600 text-sm flex items-center justify-center gap-1 mt-2",
        ),
        on_submit=DemandState.handle_submit,
        reset_on_submit=True,
        class_name="grid grid-cols-2 gap-x-4 gap-y-2 p-4 border-b bg-gray-50",
    )


def demand_list_item(demand: Demand) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(f"ZIP: {demand['zip_code']}", class_name="font-semibold"),
            rx.el.span(f"{demand['units_demanded']} units"),
            class_name="flex flex-col text-sm flex-1",
        ),
        rx.el.button(
            rx.icon(tag="trash-2", size=18),
            on_click=lambda: DemandState.remove_demand(demand["demand_id"]),
            class_name="p-1 text-red-500 hover:text-red-700",
        ),
        class_name="flex items-center justify-between p-2 rounded-md hover:bg-gray-100",
    )


def demand_list() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            f"Demand Points for: {DemandSetState.current_demand_set_name}",
            class_name="font-semibold text-md px-4 pt-4",
        ),
        rx.el.div(
            rx.foreach(DemandState.demands, demand_list_item),
            class_name="flex flex-col p-2",
        ),
        class_name="flex-1 overflow-y-auto",
    )