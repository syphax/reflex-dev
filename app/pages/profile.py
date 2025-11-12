import reflex as rx
from app.states.auth_state import AuthState
from app.components.sidebar import header


def profile_page() -> rx.Component:
    return rx.el.div(
        header(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.h1("User Profile", class_name="text-2xl font-bold"),
                    rx.el.a(
                        "Back to Dashboard",
                        href="/",
                        class_name="text-sm text-violet-600 hover:underline",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.dt(
                                "Username",
                                class_name="text-sm font-medium text-gray-500",
                            ),
                            rx.el.dd(
                                AuthState.user_info.username,
                                class_name="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0",
                            ),
                            class_name="py-4 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0",
                        ),
                        rx.el.div(
                            rx.el.dt(
                                "Email Address",
                                class_name="text-sm font-medium text-gray-500",
                            ),
                            rx.el.dd(
                                AuthState.user_info.email,
                                class_name="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0",
                            ),
                            class_name="py-4 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0",
                        ),
                        rx.el.div(
                            rx.el.dt(
                                "Member Since",
                                class_name="text-sm font-medium text-gray-500",
                            ),
                            rx.el.dd(
                                AuthState.user_info.created_at.to_string(),
                                class_name="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0",
                            ),
                            class_name="py-4 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0",
                        ),
                        class_name="divide-y divide-gray-100",
                    ),
                    class_name="mt-6 border-t border-gray-100",
                ),
                class_name="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow",
            ),
            class_name="py-12",
        ),
        class_name="min-h-screen bg-gray-100 font-['Inter']",
    )