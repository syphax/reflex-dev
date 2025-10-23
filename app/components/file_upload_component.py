import reflex as rx
from app.states.file_state import FileState


def file_upload_component() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Import Facilities", class_name="font-semibold text-lg px-4 pt-4"),
        rx.el.div(
            rx.upload.root(
                rx.el.div(
                    rx.icon("cloud_upload", class_name="w-8 h-8 text-gray-400"),
                    rx.el.p("Drop files here or click to upload"),
                    rx.el.p(".csv, .parquet", class_name="text-xs text-gray-500"),
                    class_name="flex flex-col items-center justify-center p-4 border-2 border-dashed rounded-lg text-center cursor-pointer hover:bg-gray-50",
                ),
                id="upload_facilities",
                multiple=True,
                accept={
                    "text/csv": [".csv"],
                    "application/vnd.apache.parquet": [".parquet"],
                },
                class_name="w-full",
            ),
            rx.el.div(
                rx.foreach(
                    rx.selected_files("upload_facilities"),
                    lambda file: rx.el.div(
                        rx.icon("file-text", class_name="w-4 h-4"),
                        rx.el.span(file, class_name="truncate"),
                        class_name="flex items-center gap-2 text-sm bg-gray-100 p-1 rounded",
                    ),
                ),
                class_name="flex flex-col gap-1 mt-2 text-sm",
            ),
            rx.cond(
                FileState.uploading,
                rx.el.div(
                    rx.el.progress(
                        value=FileState.upload_progress, class_name="w-full"
                    ),
                    rx.el.p(f"Uploading... {FileState.upload_progress}%"),
                    class_name="flex items-center gap-2 mt-2",
                ),
                rx.el.button(
                    "Import",
                    on_click=FileState.handle_upload(
                        rx.upload_files(upload_id="upload_facilities")
                    ),
                    class_name="w-full bg-violet-600 text-white p-2 rounded-md mt-4 hover:bg-violet-700",
                ),
            ),
            class_name="p-4",
        ),
        class_name="border-b",
    )