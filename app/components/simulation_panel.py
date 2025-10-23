import reflex as rx
from app.states.simulation_state import SimulationState
from app.states.scenario_state import ScenarioState
from app.states.map_state import FACILITY_COLORS
from app.components.export import export_button


def simulation_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Analysis & Optimization", class_name="font-semibold text-lg"),
            class_name="px-4 pt-4",
        ),
        save_scenario_form(),
        simulation_runner(),
        optimization_runner(),
        export_button(),
        rx.cond(
            SimulationState.error_message != "",
            rx.el.div(
                rx.el.p("Error:", class_name="font-semibold text-red-600"),
                rx.el.p(
                    SimulationState.error_message, class_name="text-sm text-red-600"
                ),
                class_name="m-4 p-4 bg-red-50 border border-red-200 rounded-lg",
            ),
            rx.el.div(),
        ),
        rx.cond(
            SimulationState.optimization_result.is_not_none(),
            optimization_results_display(),
            rx.el.div(),
        ),
        rx.cond(
            SimulationState.simulation_result.is_not_none(),
            simulation_results_display(),
            rx.el.div(
                rx.el.p(
                    "Run a simulation or optimization to see results.",
                    class_name="text-center text-gray-500 p-8",
                )
            ),
        ),
        class_name="flex-1 overflow-y-auto divide-y",
    )


def save_scenario_form() -> rx.Component:
    return rx.el.div(
        rx.el.h4("Save Scenario", class_name="font-semibold text-md"),
        rx.el.p(
            "Save the current network configuration and results for later comparison.",
            class_name="text-sm text-gray-600 mt-1",
        ),
        rx.el.div(
            rx.el.input(
                placeholder="Enter scenario name...",
                on_change=ScenarioState.set_new_scenario_name,
                class_name="flex-grow p-2 border rounded-l-md text-sm",
                default_value=ScenarioState.new_scenario_name,
            ),
            rx.el.button(
                rx.icon("save", class_name="mr-2"),
                "Save",
                on_click=ScenarioState.save_current_scenario,
                class_name="bg-blue-600 text-white p-2 rounded-r-md hover:bg-blue-700 flex items-center",
            ),
            class_name="flex mt-2",
        ),
        class_name="p-4",
    )


def simulation_runner() -> rx.Component:
    return rx.el.div(
        rx.el.h4("Simulation", class_name="font-semibold text-md"),
        rx.el.p(
            "Calculate network costs and service levels for the current configuration.",
            class_name="text-sm text-gray-600 mt-1",
        ),
        rx.el.button(
            rx.cond(
                SimulationState.is_simulating,
                rx.fragment(
                    rx.icon("loader", class_name="animate-spin mr-2"), "Simulating..."
                ),
                rx.fragment(rx.icon("play", class_name="mr-2"), "Run Simulation"),
            ),
            on_click=SimulationState.run_simulation,
            disabled=SimulationState.is_simulating | SimulationState.is_optimizing,
            class_name="w-full bg-green-600 text-white p-2 rounded-md mt-4 hover:bg-green-700 flex items-center justify-center disabled:bg-gray-400",
        ),
        rx.cond(
            SimulationState.is_simulating,
            rx.el.div(
                rx.el.progress(
                    value=SimulationState.simulation_progress, class_name="w-full mt-2"
                ),
                class_name="pt-2",
            ),
            rx.el.div(),
        ),
        class_name="p-4",
    )


def optimization_runner() -> rx.Component:
    return rx.el.div(
        rx.el.h4("Optimization", class_name="font-semibold text-md"),
        rx.el.p(
            "Find the optimal set of facilities to minimize total network cost.",
            class_name="text-sm text-gray-600 mt-1",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Number of DCs to Select (X)", class_name="text-sm font-medium"
                ),
                rx.el.input(
                    type="number",
                    default_value=SimulationState.num_dcs_to_select.to_string(),
                    on_change=SimulationState.set_num_dcs_to_select,
                    class_name="w-full p-1 border rounded-md text-sm",
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Candidate Facility Type", class_name="text-sm font-medium"
                ),
                rx.el.select(
                    rx.foreach(
                        list(FACILITY_COLORS.keys()), lambda t: rx.el.option(t, value=t)
                    ),
                    value=SimulationState.candidate_facility_type,
                    on_change=SimulationState.set_candidate_facility_type,
                    class_name="w-full p-1.5 border rounded-md text-sm bg-white",
                ),
            ),
            class_name="grid grid-cols-2 gap-4 mt-4",
        ),
        rx.el.button(
            rx.cond(
                SimulationState.is_optimizing,
                rx.fragment(
                    rx.icon("loader", class_name="animate-spin mr-2"), "Optimizing..."
                ),
                rx.fragment(rx.icon("sparkles", class_name="mr-2"), "Optimize Network"),
            ),
            on_click=SimulationState.run_optimization,
            disabled=SimulationState.is_optimizing | SimulationState.is_simulating,
            class_name="w-full bg-purple-600 text-white p-2 rounded-md mt-4 hover:bg-purple-700 flex items-center justify-center disabled:bg-gray-400",
        ),
        rx.cond(
            SimulationState.is_optimizing,
            rx.el.div(
                rx.el.progress(
                    value=SimulationState.optimization_progress,
                    class_name="w-full mt-2",
                ),
                rx.el.p(f"Progress: {SimulationState.optimization_progress:.0f}%"),
                class_name="pt-2 text-center text-sm",
            ),
            rx.el.div(),
        ),
        class_name="p-4",
    )


def optimization_results_display() -> rx.Component:
    return rx.el.div(
        rx.el.h4(
            "Optimization Results", class_name="font-semibold text-md px-4 pt-4 mb-2"
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("award", class_name="w-6 h-6 text-green-600"),
                    class_name="p-2 bg-green-100 rounded-full",
                ),
                rx.el.div(
                    rx.el.p("Optimal Cost", class_name="text-sm text-gray-500"),
                    rx.el.p(
                        f"${SimulationState.optimization_result['best_cost']:,.0f}",
                        class_name="text-lg font-bold",
                    ),
                ),
                rx.el.div(
                    rx.el.p("Cost Savings", class_name="text-sm text-gray-500"),
                    rx.el.p(
                        f"${SimulationState.optimization_result['cost_savings']:,.0f}",
                        class_name="text-lg font-bold text-green-600",
                    ),
                ),
                class_name="flex items-center gap-4 p-4 bg-gray-50 rounded-lg",
            ),
            rx.el.div(
                rx.el.h5(
                    "Optimal Facility Set", class_name="font-semibold mt-4 mb-2 text-sm"
                ),
                rx.el.div(
                    rx.foreach(
                        SimulationState.optimization_result["optimal_facilities"],
                        lambda facility: rx.el.div(
                            rx.icon("map-pin", class_name="w-4 h-4 text-gray-500"),
                            rx.el.span(facility),
                            class_name="flex items-center gap-2 bg-gray-100 p-2 rounded-md text-sm",
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-2",
                ),
            ),
            class_name="space-y-2",
        ),
        class_name="p-4",
    )


def simulation_results_display() -> rx.Component:
    return rx.el.div(
        rx.el.h4("Dashboard", class_name="font-semibold text-md px-4 pt-4 mb-2"),
        rx.el.div(
            metric_card(
                "Total Network Cost",
                f"${SimulationState.simulation_result['total_cost']:,.0f}",
                "dollar-sign",
            ),
            metric_card(
                "Cost Per Unit",
                f"${SimulationState.simulation_result['total_cost'] / SimulationState.simulation_result['total_demand_units']:.2f}",
                "package",
            ),
            metric_card(
                "Total Demand Units",
                f"{SimulationState.simulation_result['total_demand_units']:,}",
                "users",
            ),
            metric_card(
                "Avg Inbound Dist.",
                f"{SimulationState.simulation_result['avg_inbound_dist']:.0f} mi",
                "truck",
            ),
            metric_card(
                "Avg Outbound Dist.",
                f"{SimulationState.simulation_result['avg_outbound_dist']:.0f} mi",
                "send",
            ),
            class_name="grid grid-cols-2 gap-4",
        ),
        rx.el.div(
            cost_breakdown_card(),
            service_level_card(),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4",
        ),
        facility_utilization_card(),
        class_name="p-4 space-y-4",
    )


def metric_card(title: str, value: str, icon_name: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon_name, class_name="w-5 h-5 text-gray-500"),
            class_name="p-2 bg-gray-100 rounded-lg",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm text-gray-600"),
            rx.el.p(value, class_name="text-lg font-bold text-gray-800"),
            class_name="flex-1",
        ),
        class_name="flex items-center gap-4 p-3 border rounded-lg bg-white",
    )


def cost_breakdown_card() -> rx.Component:
    return rx.el.div(
        rx.el.h5("Cost Breakdown", class_name="font-semibold mb-2"),
        rx.el.div(
            rx.el.p("Inbound", class_name="font-medium"),
            rx.el.p(
                f"${SimulationState.simulation_result['cost_breakdown']['inbound']:,.0f}"
            ),
            class_name="flex justify-between text-sm",
        ),
        rx.el.div(
            rx.el.p("Outbound", class_name="font-medium"),
            rx.el.p(
                f"${SimulationState.simulation_result['cost_breakdown']['outbound']:,.0f}"
            ),
            class_name="flex justify-between text-sm mt-1",
        ),
        class_name="p-4 border rounded-lg bg-white",
    )


def service_level_card() -> rx.Component:
    return rx.el.div(
        rx.el.h5("Service Level (% of Demand)", class_name="font-semibold mb-2"),
        rx.el.div(
            rx.el.p("< 24 Hours", class_name="font-medium"),
            rx.el.p(
                f"{SimulationState.simulation_result['service_levels']['<24h']:.1f}%"
            ),
            class_name="flex justify-between text-sm text-green-700",
        ),
        rx.el.div(
            rx.el.p("< 48 Hours", class_name="font-medium"),
            rx.el.p(
                f"{SimulationState.simulation_result['service_levels']['<48h']:.1f}%"
            ),
            class_name="flex justify-between text-sm text-yellow-700 mt-1",
        ),
        rx.el.div(
            rx.el.p(">= 48 Hours", class_name="font-medium"),
            rx.el.p(
                f"{SimulationState.simulation_result['service_levels']['>=48h']:.1f}%"
            ),
            class_name="flex justify-between text-sm text-red-700 mt-1",
        ),
        class_name="p-4 border rounded-lg bg-white",
    )


def facility_utilization_card() -> rx.Component:
    return rx.el.div(
        rx.el.h5("Facility Utilization (Top 5)", class_name="font-semibold mb-2"),
        rx.foreach(
            SimulationState.sorted_facility_utilization,
            lambda item: rx.el.div(
                rx.el.p(item[0], class_name="truncate"),
                rx.el.p(f"{item[1]:,} units", class_name="font-semibold"),
                class_name="flex justify-between items-center text-sm p-2 bg-gray-50 rounded",
            ),
        ),
        class_name="p-4 border rounded-lg bg-white",
    )