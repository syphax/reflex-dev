import reflex as rx
import reflex_enterprise as rxe
from app.states.map_state import MapState, FACILITY_COLORS


def map_component() -> rx.Component:
    return rxe.map(
        rxe.map.tile_layer(
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            z_index=1,
        ),
        rx.foreach(
            MapState.facility_markers,
            lambda marker: rxe.map.circle_marker(
                rxe.map.tooltip(marker["tooltip"]),
                center=marker["position"],
                radius=8,
                path_options=rxe.map.path_options(
                    color=marker["color"], fill_color=marker["color"], fill_opacity=0.8
                ),
                draggable=True,
                event_handlers={
                    "dragend": lambda event, payload: MapState.update_facility_location(
                        payload
                    )
                },
                facility_id=marker["facility_id"],
            ),
        ),
        id="map",
        center=MapState.center,
        zoom=MapState.zoom,
        on_click=lambda e: MapState.add_facility(e),
        height="100%",
        width="100%",
        class_name="rounded-lg shadow-md",
    )