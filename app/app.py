import reflex as rx
import reflex_enterprise as rxe
from app.components.sidebar import sidebar
from app.components.map_component import map_component
from app.pages.edit_sites import edit_sites_page


def index() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            sidebar(),
            rx.el.div(map_component(), class_name="flex-1 h-screen p-4 bg-gray-100"),
            class_name="flex w-screen h-screen",
        ),
        class_name="font-['Inter']",
    )


from app.states.map_state import MapState

app = rxe.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
        rx.el.link(
            rel="stylesheet",
            href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
            integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=",
            cross_origin="",
        ),
    ],
)
app.add_page(index, route="/", on_load=MapState.on_load)
app.add_page(edit_sites_page, route="/edit-sites")