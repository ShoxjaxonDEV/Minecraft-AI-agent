import pyautogui
import time

input_mod = pyautogui

class MinecraftController:
    def __init__(self):
        # Пауза между командами, чтобы не спамить слишком быстро
        input_mod.PAUSE = 0.05

    def move_forward(self, duration=0.5):
        input_mod.keyDown('w')
        time.sleep(duration)
        input_mod.keyUp('w')

    def move_back(self, duration=0.5):
        input_mod.keyDown('s')
        time.sleep(duration)
        input_mod.keyUp('s')

    def move_left(self, duration=0.5):
        input_mod.keyDown('a')
        time.sleep(duration)
        input_mod.keyUp('a')

    def move_right(self, duration=0.5):
        input_mod.keyDown('d')
        time.sleep(duration)
        input_mod.keyUp('d')

    def shift(self):
        input_mod.press('shift')

    def jump(self):
        input_mod.press('space')

    def attack(self, duration=1.0):
        input_mod.click("right")

    def turn_left(self, degrees=30):
        # Интенсивность подбирается под чувствительность мыши в игре
        move_x = int(degrees * 5)
        input_mod.moveRel(-move_x, 0)

    def turn_right(self, degrees=30):
        move_x = int(degrees * 5)
        input_mod.moveRel(move_x, 0)

    def use_item(self):
        input_mod.click(button='right')

    def open_inventory(self):
        input_mod.press('e')

if __name__ == "__main__":
    agent = MinecraftController()
    agent.move_forward()