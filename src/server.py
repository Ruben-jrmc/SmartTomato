from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
import uvicorn
import requests
from fastapi.middleware.cors import CORSMiddleware
import io


class Server:
    def __init__(self,  vid_frame_generator, stm_interface, journal,
                 static_image_path="static/output/photo.jpg"):
        self.app = FastAPI()
        self.last_pred_class = 0
        self.static_image_path = static_image_path
        self.threshold_inc = True
        self.vid_frame_generator = vid_frame_generator
        self.time_tomato_in_band = 0
        self.tomatos_by_minute = 0
        self.stm_interface = stm_interface
        self.journal = journal

        # Para testeo no se si en prod
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:5173"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @self.app.post("/sthreshold")
        def set_threshold(threshold: int):
            self.threshold_inc = threshold

        @self.app.post("/slclass")
        def set_class(pred_class: int):
            self.last_pred_class = pred_class

        @self.app.get("/glclass")
        def get_class():
            return self.last_pred_class

        @self.app.get("/gttInBand")
        def get_ttInBand():
            return self.time_tomato_in_band

        @self.app.post("/sttInBand")
        def set_ttInBand(time_tomato_in_band: int):
            self.time_tomato_in_band = time_tomato_in_band

        @self.app.get("/gtbMin")
        def get_tbMin():
            return self.tomatos_by_minute

        @self.app.get("/journal")
        def get_journal():
            buff = io.StringIO(self.journal.journal.to_csv())
            return StreamingResponse(buff, media_type="text/csv",
                                     headers={
                                         "Content-Disposition":
                                         "attachment; filename=journal.csv"})

        @self.app.post("/stbMin")
        def set_tbMin(tomatos_by_minute: int):
            self.tomatos_by_minute = tomatos_by_minute

        @self.app.get("/glpImg")
        def get_image():
            if self.static_image_path:
                return FileResponse(
                    self.static_image_path, media_type="image/jpeg")
            else:
                raise HTTPException(
                    status_code=404,
                    detail="Aun no se ah generado ninguna imagen")

        @self.app.post("/toggleBar")
        def toggleBar():
            self.stm_interface.toggleBand()

        @self.app.get("/video")
        def video_feed():
            return StreamingResponse(self.vid_frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")

    def start(self, host="0.0.0.0", port=8000):
        uvicorn.run(self.app, host=host, port=port)

    def update_parameters(self, last_pred_class=None, time_tomato_in_band=None, tomatos_by_minute=None):
        if last_pred_class:
            data = {"pred_class": int(last_pred_class)}
            response = requests.post(
                "http://127.0.0.1:8000/slclass", params=data)
            print(response)
        if time_tomato_in_band:
            data = {"time_tomato_in_band": int(time_tomato_in_band)}
            response = requests.post(
                "http://127.0.0.1:8000/sttInBand", params=data)
            print(response)
        if tomatos_by_minute:
            data = {"tomatos_by_minute": int(tomatos_by_minute)}
            response = requests.post(
                "http://127.0.0.1:8000/stbMin", params=data)
            print(response)

    def get_threshold(self):
        return self.threshold_inc
