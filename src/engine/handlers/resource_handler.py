import os
import pygame

from src.engine.app import App


class ResourceHandler:
    FONT = []
    IMAGE = {}
    SOUND = {}

    @classmethod
    def load(cls):
        cls.load_sound()
        cls.load_images()

    @classmethod
    def load_sound(cls):
        sound_dir = App.ASSETS_PATH+"/sound/"
        for file in os.scandir(sound_dir):
            file_path = sound_dir+file.name

            if not file.is_dir():
                cls.SOUND[file.name.split(".")[0]] = pygame.mixer.Sound(file_path)
                continue

            cls.SOUND[file.name] = {}
            for sub_file in os.scandir(file_path):
                sub_file_path = "".join([file_path, "/", sub_file.name])

                cls.SOUND[file.name][sub_file.name.split(".")[0]] = pygame.mixer.Sound(sub_file_path)

    @classmethod
    def load_images(cls):
        image_dir = App.ASSETS_PATH+"/image/"
        for file in os.scandir(image_dir):
            file_path = image_dir+file.name

            if not file.is_dir():
                cls.IMAGE[file.name.split(".")[0]] = pygame.image.load(file_path).convert()
                continue

            cls.IMAGE[file.name] = {}
            for sub_file in os.scandir(file_path):
                sub_file_path = "".join([file_path, "/", sub_file.name])

                cls.IMAGE[file.name][sub_file.name.split(".")[0]] = pygame.image.load(sub_file_path).convert()


if __name__ == '__main__':
    App.init('../../../assets')
    ResourceHandler.load()
    ResourceHandler.SOUND["blip"].play()
