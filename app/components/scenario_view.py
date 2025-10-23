import reflex as rx
from app.states.scenario_state import ScenarioState, Scenario


def scenario_view() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Scenario Comparison", class_name="font-semibold text-lg px-4 pt-4"),
        rx.cond(
            ScenarioState.scenarios.length() > 0,
            rx.el.div(
                rx.el.table(
                    scenario_table_header(),
                    scenario_table_body(),
                    class_name="min-w-full divide-y divide-gray-200",
                ),
                class_name="border rounded-lg overflow-auto m-4",
            ),
            rx.el.div(
                rx.icon("folder-search", class_name="w-12 h-12 text-gray-400"),
                rx.el.p("No scenarios saved yet.", class_name="text-gray-500 mt-2"),
                rx.el.p(
                    "Run a simulation and click 'Save Scenario' to get started.",
                    class_name="text-sm text-gray-500",
                ),
                class_name="flex flex-col items-center justify-center h-64 text-center",
            ),
        ),
        class_name="flex-1 overflow-y-auto",
    )


def scenario_table_header() -> rx.Component:
    return rx.el.thead(
        rx.el.tr(
            rx.el.th(
                "Scenario Name",
                class_name="px-4 py-3 text-left text-sm font-semibold text-gray-600",
            ),
            rx.el.th(
                "Total Cost",
                class_name="px-4 py-3 text-left text-sm font-semibold text-gray-600",
            ),
            rx.el.th(
                "# Facilities",
                class_name="px-4 py-3 text-left text-sm font-semibold text-gray-600",
            ),
            rx.el.th(
                "Service <24h",
                class_name="px-4 py-3 text-left text-sm font-semibold text-gray-600",
            ),
            rx.el.th(
                "Avg Outbound Dist",
                class_name="px-4 py-3 text-left text-sm font-semibold text-gray-600",
            ),
            rx.el.th(
                "Actions",
                class_name="px-4 py-3 text-left text-sm font-semibold text-gray-600",
            ),
            class_name="bg-gray-50",
        )
    )


def scenario_table_body() -> rx.Component:
    return rx.el.tbody(
        rx.foreach(ScenarioState.scenarios, scenario_table_row),
        class_name="bg-white divide-y divide-gray-200",
    )


def scenario_table_row(scenario: Scenario) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            scenario["name"], class_name="px-4 py-3 whitespace-nowrap font-medium"
        ),
        rx.el.td(
            rx.cond(
                scenario["simulation_result"],
                f"${scenario['simulation_result']['total_cost']:,.0f}",
                "N/A",
            ),
            class_name="px-4 py-3 whitespace-nowrap",
        ),
        rx.el.td(
            scenario["facilities"].length().to_string(),
            class_name="px-4 py-3 whitespace-nowrap",
        ),
        rx.el.td(
            rx.cond(
                scenario["simulation_result"],
                f"{scenario['simulation_result']['service_levels']['<24h']:.1f}%",
                "N/A",
            ),
            class_name="px-4 py-3 whitespace-nowrap",
        ),
        rx.el.td(
            rx.cond(
                scenario["simulation_result"],
                f"{scenario['simulation_result']['avg_outbound_dist']:.0f} mi",
                "N/A",
            ),
            class_name="px-4 py-3 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.button(
                rx.icon("trash-2", size=16),
                on_click=lambda: ScenarioState.remove_scenario(scenario["scenario_id"]),
                class_name="p-1.5 text-red-500 hover:bg-red-100 rounded-md",
            ),
            class_name="px-4 py-3 whitespace-nowrap",
        ),
        class_name="hover:bg-gray-50 text-sm",
    )