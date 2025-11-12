import reflex as rx
from app.states.facility_editor_state import FacilityEditorState, ALL_FACILITY_TYPES


def facility_editor_panel() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Facility Editor", class_name="font-semibold text-lg px-4 pt-4"),
        rx.cond(
            FacilityEditorState.selected_facility_id.is_not_none(),
            rx.cond(
                FacilityEditorState.edited_facility.is_not_none(),
                editable_facility_form(),
                rx.el.div(
                    rx.icon("loader", class_name="animate-spin"),
                    class_name="flex justify-center items-center h-full",
                ),
            ),
            rx.el.div(
                rx.icon("mouse-pointer-click", class_name="w-12 h-12 text-gray-400"),
                rx.el.p(
                    "No facility selected",
                    class_name="text-gray-500 mt-2 font-semibold",
                ),
                rx.el.p(
                    "Click on a facility on the map to edit its details.",
                    class_name="text-sm text-gray-500 text-center",
                ),
                class_name="flex flex-col items-center justify-center h-full p-4",
            ),
        ),
        class_name="flex-1 overflow-y-auto",
    )


def editable_facility_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            editor_input_field(
                "Site Name",
                "site_name",
                FacilityEditorState.edited_facility["site_name"],
            ),
            editor_input_field(
                "Parent Company",
                "parent_company",
                FacilityEditorState.edited_facility["parent_company"],
            ),
            editor_input_field(
                "Street Address",
                "street_address",
                FacilityEditorState.edited_facility["street_address"],
            ),
            editor_input_field(
                "City", "city", FacilityEditorState.edited_facility["city"]
            ),
            editor_input_field(
                "State/Province",
                "state_province",
                FacilityEditorState.edited_facility["state_province"],
            ),
            editor_input_field(
                "ZIP Code", "zip5", FacilityEditorState.edited_facility["zip5"]
            ),
            class_name="grid grid-cols-2 gap-4 p-4 border-b",
        ),
        facility_type_selector(),
        rx.el.div(
            rx.el.button(
                "Save Changes",
                on_click=FacilityEditorState.save_changes,
                class_name="w-full bg-violet-600 text-white p-2 rounded-md hover:bg-violet-700",
            ),
            class_name="p-4",
        ),
        class_name="flex flex-col h-full",
    )


def editor_input_field(label: str, field_name: str, value: rx.Var) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="text-sm font-medium text-gray-700"),
        rx.el.input(
            default_value=value,
            on_change=lambda val: FacilityEditorState.handle_edit(field_name, val),
            class_name="w-full p-1.5 border rounded-md text-sm mt-1",
        ),
        class_name="col-span-1",
    )


def facility_type_selector() -> rx.Component:
    return rx.el.div(
        rx.el.h4("Facility Types", class_name="font-semibold text-md mb-2"),
        rx.el.div(
            rx.foreach(
                ALL_FACILITY_TYPES,
                lambda f_type: rx.el.label(
                    rx.el.input(
                        type="checkbox",
                        checked=FacilityEditorState.edited_facility[
                            "facility_types"
                        ].contains(f_type),
                        on_change=lambda _: FacilityEditorState.toggle_facility_type(
                            f_type
                        ),
                        class_name="mr-2 rounded",
                    ),
                    f_type,
                    class_name="flex items-center text-sm",
                ),
            ),
            class_name="grid grid-cols-2 gap-2",
        ),
        class_name="p-4",
    )