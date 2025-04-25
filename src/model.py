from ultralytics import YOLO

model = YOLO("model/best.pt")


class Model:
    def __init__(self, output_dir="static/", output_name="output/"):
        self.output_dir = output_dir
        self.output_name = output_name

    def predict(self, path) -> int:
        result = model(path, save=True, exist_ok=True,
                       project=self.output_dir, name=self.output_name)
        r = result[0]
        class_ids = r.boxes.cls.cpu().numpy().astype(int)
        print("Prediccion hecha")
        return (class_ids)
