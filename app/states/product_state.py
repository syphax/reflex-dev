import reflex as rx
import uuid
from typing import Literal, TypedDict, Callable
import logging

UnitSystem = Literal["English", "Metric"]
WeightUnit = Literal["lb", "kg"]
CubeUnit = Literal["cu ft", "cu m"]


class Product(TypedDict):
    product_id: str
    product_name: str
    cost_per_unit: float
    price_per_unit: float
    weight_per_unit: float
    weight_unit: WeightUnit
    cube_per_unit: float
    cube_unit: CubeUnit


DEFAULT_PRODUCTS: list[Product] = [
    {
        "product_id": str(uuid.uuid4()),
        "product_name": "Standard Widget",
        "cost_per_unit": 1.0,
        "price_per_unit": 2.0,
        "weight_per_unit": 1.0,
        "weight_unit": "lb",
        "cube_per_unit": 1.0,
        "cube_unit": "cu ft",
    }
]


class ProductState(rx.State):
    products: list[Product] = DEFAULT_PRODUCTS
    unit_system: UnitSystem = "English"
    new_product_name: str = ""
    new_product_cost: float = 0.0
    new_product_price: float = 0.0
    new_product_weight: float = 0.0
    new_product_cube: float = 0.0
    search_query: str = ""
    sort_by: str = "product_name"
    sort_order: str = "asc"

    @rx.event
    def add_product(self):
        if not self.new_product_name:
            return rx.toast.error("Product name cannot be empty.")
        new_prod = Product(
            product_id=str(uuid.uuid4()),
            product_name=self.new_product_name,
            cost_per_unit=self.new_product_cost,
            price_per_unit=self.new_product_price,
            weight_per_unit=self.new_product_weight,
            weight_unit="lb" if self.unit_system == "English" else "kg",
            cube_per_unit=self.new_product_cube,
            cube_unit="cu ft" if self.unit_system == "English" else "cu m",
        )
        self.products.append(new_prod)
        self.new_product_name = ""
        self.new_product_cost = 0.0
        self.new_product_price = 0.0
        self.new_product_weight = 0.0
        self.new_product_cube = 0.0

    @rx.event
    def remove_product(self, product_id: str):
        self.products = [p for p in self.products if p["product_id"] != product_id]

    @rx.event
    def edit_product_field(self, product_id: str, field: str, value: str):
        for i, p in enumerate(self.products):
            if p["product_id"] == product_id:
                if field in [
                    "cost_per_unit",
                    "price_per_unit",
                    "weight_per_unit",
                    "cube_per_unit",
                ]:
                    try:
                        self.products[i][field] = float(value)
                    except ValueError as e:
                        logging.exception(f"Error: {e}")
                        return rx.toast.error(f"Invalid number for {field}")
                else:
                    self.products[i][field] = value
                return

    @rx.event
    def set_sort_column(self, column: str):
        if self.sort_by == column:
            self.sort_order = "desc" if self.sort_order == "asc" else "asc"
        else:
            self.sort_by = column
            self.sort_order = "asc"

    @rx.var
    def filtered_and_sorted_products(self) -> list[Product]:
        products = self.products
        if self.search_query:
            search_lower = self.search_query.lower()
            products = [
                p for p in products if search_lower in p["product_name"].lower()
            ]

        @rx.event
        def sort_key(p: Product):
            value = p.get(self.sort_by)
            if isinstance(value, (int, float)):
                return value
            return str(value if value is not None else "")

        reverse = self.sort_order == "desc"
        return sorted(products, key=sort_key, reverse=reverse)

    @rx.event
    def toggle_unit_system(self):
        if self.unit_system == "English":
            self.unit_system = "Metric"
            for i, p in enumerate(self.products):
                self.products[i]["weight_per_unit"] *= 0.453592
                self.products[i]["weight_unit"] = "kg"
                self.products[i]["cube_per_unit"] *= 0.0283168
                self.products[i]["cube_unit"] = "cu m"
        else:
            self.unit_system = "English"
            for i, p in enumerate(self.products):
                self.products[i]["weight_per_unit"] /= 0.453592
                self.products[i]["weight_unit"] = "lb"
                self.products[i]["cube_per_unit"] /= 0.0283168
                self.products[i]["cube_unit"] = "cu ft"

    @rx.var
    def weight_unit_label(self) -> str:
        return "kg" if self.unit_system == "Metric" else "lb"

    @rx.var
    def cube_unit_label(self) -> str:
        return "cu m" if self.unit_system == "Metric" else "cu ft"