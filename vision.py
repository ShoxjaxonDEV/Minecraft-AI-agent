from ultralytics import YOLO
import os

# results = model.train(data="", epochs=100, imgsz=640)

class MinecraftVision:
    #подключение модели
    # def __init__(self):
    #     self.model = YOLO("yolo11n.pt")
    #
    # def train_mine(self):
    #     # Метод, который запустит обучение на наших блоках
    #     print("Start training")
    #     self.model.train(
    #         data = 'dataset/data.yaml',
    #         epochs = 15,
    #         imgsz = 320,
    #         workers=1,  # СТРОГО 1 поток. Это оставит остальные потоки процессора для работы самой Windows
    #         #batch=2,    # Берем картинки крошечными порциями (по 2 штуки), чтобы не забивать оперативку
    #         cache=False,    # Отключаем кэширование в память, чтобы ноут не вис из-за нехватки ОЗУ
    #         device = 'cpu'
    #     )
    def __init__(self):
        # model = YOLO("yolo11n.pt")
        # model.export(format="openvino")
        # Прописываем точный путь к твоей обученной модели
        self.model_path = os.path.join(
            os.getcwd(),
            "runs", "detect", "train-6", "weights", "best.pt"
        )
        print(f"Загрузка обученной модели из: {self.model_path}")
        self.model = YOLO(self.model_path)

    def detect(self, frame):
        result = self.model(frame, verbose=False, conf=0.5, imgsz=320)
        results = result[0]
        return results


if __name__ == "__main__":
    # Этот блок сработает, только если запустить именно vision.py напрямую
    agent = MinecraftVision()
    agent.train_mine()