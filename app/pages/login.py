import reflex as rx
from app.states.auth_state import AuthState


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("network", class_name="h-10 w-10 text-violet-600"),
                rx.el.h2(
                    "Log in to your account",
                    class_name="mt-6 text-2xl font-bold tracking-tight text-gray-900",
                ),
                rx.el.p(
                    "Or ",
                    rx.el.a(
                        "create an account",
                        href="/register",
                        class_name="font-medium text-violet-600 hover:text-violet-500",
                    ),
                    class_name="mt-2 text-sm text-gray-600",
                ),
                class_name="sm:mx-auto sm:w-full sm:max-w-md text-center",
            ),
            rx.el.div(
                rx.el.form(
                    rx.el.div(
                        rx.el.label(
                            "Email address",
                            html_for="email",
                            class_name="block text-sm font-medium leading-6 text-gray-900",
                        ),
                        rx.el.input(
                            type="email",
                            id="email",
                            name="email",
                            required=True,
                            class_name="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-violet-600 sm:text-sm sm:leading-6 mt-2",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Password",
                            html_for="password",
                            class_name="block text-sm font-medium leading-6 text-gray-900",
                        ),
                        rx.el.input(
                            type="password",
                            id="password",
                            name="password",
                            required=True,
                            class_name="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-violet-600 sm:text-sm sm:leading-6 mt-2",
                        ),
                        class_name="mb-6",
                    ),
                    rx.cond(
                        AuthState.error_message != "",
                        rx.el.div(
                            rx.el.p(
                                AuthState.error_message,
                                class_name="text-sm text-red-600",
                            ),
                            class_name="mb-4 p-3 bg-red-50 border border-red-200 rounded-md",
                        ),
                    ),
                    rx.el.button(
                        "Sign in",
                        type="submit",
                        class_name="flex w-full justify-center rounded-md bg-violet-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-violet-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-violet-600",
                    ),
                    on_submit=AuthState.login,
                ),
                class_name="mt-10 sm:mx-auto sm:w-full sm:max-w-md bg-white px-6 py-8 shadow sm:rounded-lg sm:px-10",
            ),
            class_name="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8",
        ),
        class_name="bg-gray-50",
    )