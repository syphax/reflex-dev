import reflex as rx
import reflex_enterprise as rxe
from app.components.sidebar import sidebar
from app.components.map_component import map_component
from app.pages.edit_sites import edit_sites_page
from app.pages.login import login_page
from app.pages.register import registration_page
from app.pages.profile import profile_page
from app.pages.my_networks import my_networks_page
from app.states.auth_state import AuthState, require_login
from app.states.map_state import MapState


def index() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            sidebar(),
            rx.el.div(map_component(), class_name="flex-1 h-screen p-4 bg-gray-100"),
            class_name="flex w-screen h-screen",
        ),
        class_name="font-['Inter']",
    )


async def on_load_index():
    yield require_login
    yield MapState.on_load()


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
app.add_page(index, route="/", on_load=on_load_index)
app.add_page(edit_sites_page, route="/edit-sites", on_load=require_login)
app.add_page(my_networks_page, route="/my-networks", on_load=require_login)
app.add_page(login_page, route="/login")
app.add_page(registration_page, route="/register")
app.add_page(profile_page, route="/profile", on_load=require_login)