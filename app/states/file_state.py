import reflex as rx
from app.states.map_state import MapState, Facility
import pandas as pd
import pyarrow.parquet as pq
import io
import logging


class FileState(rx.State):
    uploading: bool = False
    upload_progress: int = 0

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        if not files:
            yield rx.toast.error("No files selected.")
            return
        self.uploading = True
        self.upload_progress = 0
        try:
            map_state = await self.get_state(MapState)
            for i, file in enumerate(files):
                upload_data = await file.read()
                df = None
                if file.name.endswith(".csv"):
                    df = pd.read_csv(io.BytesIO(upload_data))
                elif file.name.endswith(".parquet"):
                    df = pq.read_table(io.BytesIO(upload_data)).to_pandas()
                else:
                    yield rx.toast.error(f"Unsupported file type: {file.name}")
                    continue
                required_cols = [
                    "site_name",
                    "parent_company",
                    "street_address",
                    "state_province",
                    "zip5",
                    "zip9",
                    "country",
                    "latitude",
                    "longitude",
                    "facility_type",
                ]
                if not all((col in df.columns for col in required_cols)):
                    yield rx.toast.error(f"Missing required columns in {file.name}")
                    continue
                new_facilities = []
                for _, row in df.iterrows():
                    new_facility = Facility(
                        facility_id=str(pd.NA)
                        if pd.isna(row.get("facility_id"))
                        else str(row.get("facility_id")),
                        facility_type=row["facility_type"],
                        site_name=row["site_name"],
                        parent_company=row["parent_company"],
                        street_address=row["street_address"],
                        city=row.get("city", ""),
                        state_province=row["state_province"],
                        zip5=str(row["zip5"]),
                        zip9=str(row["zip9"]),
                        country=row["country"],
                        latitude=float(row["latitude"]),
                        longitude=float(row["longitude"]),
                        is_active=bool(row.get("is_active", True)),
                    )
                    new_facilities.append(new_facility)
                map_state.add_facilities(new_facilities)
                self.upload_progress = int((i + 1) / len(files) * 100)
                yield
            yield rx.toast.success(f"Successfully imported {len(files)} file(s).")
        except Exception as e:
            logging.exception(f"Error: {e}")
            yield rx.toast.error(f"Upload failed: {e}")
        finally:
            self.uploading = False
            self.upload_progress = 0
            yield rx.clear_selected_files("upload_facilities")