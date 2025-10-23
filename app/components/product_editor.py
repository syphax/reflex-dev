import reflex as rx
from app.states.product_state import ProductState, Product


def product_attributes_editor() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Products", class_name="font-semibold text-lg"),
            unit_selection_toggle(),
            class_name="flex justify-between items-center px-4 pt-4",
        ),
        add_product_form(),
        product_table(),
        class_name="flex-1 overflow-y-auto",
    )


def unit_selection_toggle() -> rx.Component:
    return rx.el.div(
        rx.el.label("Units: ", class_name="text-sm font-medium"),
        rx.el.button(
            rx.el.span(
                "English",
                class_name=rx.cond(
                    ProductState.unit_system == "English", "font-bold", ""
                ),
            ),
            on_click=rx.cond(
                ProductState.unit_system == "Metric",
                ProductState.toggle_unit_system,
                rx.noop(),
            ),
            class_name=rx.cond(
                ProductState.unit_system == "English",
                "bg-violet-600 text-white",
                "bg-gray-200",
            ),
            style={
                "borderTopLeftRadius": "0.375rem",
                "borderBottomLeftRadius": "0.375rem",
                "padding": "0.25rem 0.75rem",
            },
        ),
        rx.el.button(
            rx.el.span(
                "Metric",
                class_name=rx.cond(
                    ProductState.unit_system == "Metric", "font-bold", ""
                ),
            ),
            on_click=rx.cond(
                ProductState.unit_system == "English",
                ProductState.toggle_unit_system,
                rx.noop(),
            ),
            class_name=rx.cond(
                ProductState.unit_system == "Metric",
                "bg-violet-600 text-white",
                "bg-gray-200",
            ),
            style={
                "borderTopRightRadius": "0.375rem",
                "borderBottomRightRadius": "0.375rem",
                "padding": "0.25rem 0.75rem",
            },
        ),
        class_name="flex items-center text-sm",
    )


def add_product_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.label("Product Name", class_name="text-sm font-medium"),
            rx.el.input(
                placeholder="Product Name",
                name="product_name",
                on_change=ProductState.set_new_product_name,
                class_name="w-full p-1 border rounded-md text-sm",
                default_value=ProductState.new_product_name,
            ),
            class_name="col-span-2",
        ),
        rx.el.div(
            rx.el.label("Cost", class_name="text-sm font-medium"),
            rx.el.input(
                placeholder="Cost",
                name="cost",
                type="number",
                on_change=ProductState.set_new_product_cost,
                class_name="w-full p-1 border rounded-md text-sm",
                default_value=ProductState.new_product_cost.to_string(),
            ),
        ),
        rx.el.div(
            rx.el.label("Price", class_name="text-sm font-medium"),
            rx.el.input(
                placeholder="Price",
                name="price",
                type="number",
                on_change=ProductState.set_new_product_price,
                class_name="w-full p-1 border rounded-md text-sm",
                default_value=ProductState.new_product_price.to_string(),
            ),
        ),
        rx.el.div(
            rx.el.label(
                f"Weight ({ProductState.weight_unit_label})",
                class_name="text-sm font-medium",
            ),
            rx.el.input(
                placeholder="Weight",
                name="weight",
                type="number",
                on_change=ProductState.set_new_product_weight,
                class_name="w-full p-1 border rounded-md text-sm",
                default_value=ProductState.new_product_weight.to_string(),
            ),
        ),
        rx.el.div(
            rx.el.label(
                f"Cube ({ProductState.cube_unit_label})",
                class_name="text-sm font-medium",
            ),
            rx.el.input(
                placeholder="Cube",
                name="cube",
                type="number",
                on_change=ProductState.set_new_product_cube,
                class_name="w-full p-1 border rounded-md text-sm",
                default_value=ProductState.new_product_cube.to_string(),
            ),
        ),
        rx.el.button(
            rx.icon("plus", size=16),
            "Add Product",
            on_click=ProductState.add_product,
            class_name="col-span-full bg-blue-500 text-white p-1.5 rounded-md hover:bg-blue-600 text-sm flex items-center justify-center gap-1 mt-2",
        ),
        class_name="grid grid-cols-2 gap-x-4 gap-y-2 p-4 border-b bg-gray-50",
    )


def sortable_header(label: str, column_key: str) -> rx.Component:
    return rx.el.th(
        rx.el.button(
            label,
            rx.icon(
                tag=rx.cond(ProductState.sort_order == "asc", "arrow-up", "arrow-down"),
                class_name=rx.cond(
                    ProductState.sort_by == column_key, "w-4 h-4 ml-2", "hidden"
                ),
            ),
            on_click=lambda: ProductState.set_sort_column(column_key),
            class_name="flex items-center font-medium text-gray-600 hover:text-gray-900",
        ),
        scope="col",
        class_name="px-4 py-2 text-left text-sm",
    )


def product_table() -> rx.Component:
    return rx.el.div(
        rx.el.input(
            placeholder="Search products...",
            on_change=ProductState.set_search_query.debounce(300),
            class_name="w-full px-4 py-2 border rounded-md mb-4",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        sortable_header("Product Name", "product_name"),
                        sortable_header("Cost", "cost_per_unit"),
                        sortable_header("Price", "price_per_unit"),
                        sortable_header("Weight", "weight_per_unit"),
                        sortable_header("Cube", "cube_per_unit"),
                        rx.el.th("", class_name="px-4 py-2"),
                        class_name="border-b bg-gray-50",
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        ProductState.filtered_and_sorted_products, product_editor_row
                    ),
                    class_name="divide-y divide-gray-200",
                ),
                class_name="min-w-full bg-white",
            ),
            class_name="border rounded-lg overflow-auto",
        ),
        class_name="p-4",
    )


def product_editor_row(product: Product) -> rx.Component:
    return rx.el.tr(
        rx.el.td(product["product_name"], class_name="px-4 py-2 whitespace-nowrap"),
        rx.el.td(
            f"${product['cost_per_unit']:.2f}", class_name="px-4 py-2 whitespace-nowrap"
        ),
        rx.el.td(
            f"${product['price_per_unit']:.2f}",
            class_name="px-4 py-2 whitespace-nowrap",
        ),
        rx.el.td(
            f"{product['weight_per_unit']:.2f} {product['weight_unit']}",
            class_name="px-4 py-2 whitespace-nowrap",
        ),
        rx.el.td(
            f"{product['cube_per_unit']:.2f} {product['cube_unit']}",
            class_name="px-4 py-2 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.button(
                rx.icon(tag="trash-2", size=16),
                on_click=lambda: ProductState.remove_product(product["product_id"]),
                class_name="p-1.5 text-red-500 hover:bg-red-100 rounded-md",
            ),
            class_name="px-4 py-2 text-right",
        ),
        class_name="hover:bg-gray-50",
    )