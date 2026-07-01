import time
import cv2
import mss
import numpy as np
import pygetwindow as gw
from vision import MinecraftVision
from controller import MinecraftController
from ultralytics import YOLO

controller = MinecraftController()
model = YOLO("D:/Python project/first ai/Minecraft AI agent/runs/detect/train-6/weights/best_openvino_model")


def get_minecraft_window():
    print("Ищу окно Minecraft в системе...")
    # Принудительно ищем любое окно, где есть слово minecraft
    all_windows = gw.getAllWindows()
    win = None
    for w in all_windows:
        if "minecraft" in w.title.lower():
            win = w
            break
    if not win:
        print("Окно с игрой не найдено среди запущенных процессов.")
        return None
    print(f"Найдено окно: '{win.title}'")
    if win.isMinimized:
        print("⚠ Внимание: Окно свёрнуто! Разверни его на экране.")
        return None
    # Возвращаем координаты
    return {"top": win.top, "left": win.left, "width": win.width, "height": win.height}


def start_capture():
    monitor = get_minecraft_window()
    if not monitor:
        print("Не удалось инициализировать захват экрана.")
        return
    print("Запуск стрима кадров... Нажми 'q' в окне видео для выхода.")

    vision_agent = MinecraftVision()

    with mss.MSS() as sct:
        last_time = time.time()

        frame_count = 0
        predictions = None
        while True:
            frame_count += 1
            # 1. Захват кадра
            screenshot = sct.grab(monitor)

            # 2. Конвертация в формат OpenCV
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            frame = cv2.resize(frame, (640, 480))
            # height, width = frame.shape[:2]

            if frame_count % 30 == 0:
                predictions = vision_agent.detect(frame)

            results = model(frame, verbose=False)[0]

            # Проверяем, что ИИ нашёл на картинке
            for box in results.boxes:
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                confidence = float(box.conf[0])

                if confidence > 0.5:
                    # Переводим в нижний регистр, чтобы точно совпало
                    target = class_name.lower()

                    # Если видит алмазы
                    if target == "diamond ore" or target == "iron ore":
                        print(f"Вижу алмазы ({confidence * 100:.1f}%)! Иду копать...")
                        controller.move_forward(duration=1.0)
                        controller.attack(duration=2.0)
                        break
                        # Если видит дерево
                    elif target == "Tree" or target == "wood":
                        print(f"Вижу дерево ({confidence * 100:.1f}%)! Иду рубить...")
                        controller.move_forward(duration=1.0)
                        controller.attack(duration=2.0)
                        break

            # 3. Считаем FPS
            fps = 1 / (time.time() - last_time)
            last_time = time.time()

            if predictions is not None and predictions.boxes is not None:

                for box in predictions.boxes:
                    # Извлекаем координаты и сразу переводим их в целые числа (пиксели)
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    # Извлекаем уверенность (какое-то дробное число, например, 0.85)
                    conf = float(box.conf[0])
                    # Извлекаем ID класса (например, 0, 1, 2)
                    cls_id = int(box.cls[0])
                    # Получаем имя класса по его ID из нашей модели
                    cls_name = vision_agent.model.names[cls_id]

                    # Формируем красивый текст (например: "Class 0: 0.85")
                    label = f"ID {cls_name}: {conf:.2f}"
                    # Рисуем прямоугольник (красный цвет BGR: 0, 0, 255)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # 4. Выводим FPS на картинку для теста
            cv2.putText(
                frame,
                f"FPS: {int(fps)}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

            cv2.imshow("AI Vision Test", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break
if __name__ == "__main__":
    start_capture()