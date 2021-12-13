from pathlib import Path
import shutil
import os

from tqdm import tqdm
import requests


ANNOTATION_FOLDER = Path('annotations')
DATA_FOLDER = Path('data')  # Will be created to store images


def check_or_create_folder(folder):
    if os.path.exists(folder):
        print(f"Directory {folder} already exists!")
        if len([f for f in os.listdir(folder) if os.path.isfile(folder / f)]) > 0:
            print("Folder to download images to already exists and is not empty! Not downloading.")
            return False
        return True
    else:
        os.makedirs(folder, exist_ok=True)
        return True


def get_images(train_or_val):
    training_img_links = open(ANNOTATION_FOLDER / (train_or_val + '.txt')).read().splitlines()
    for img_link in tqdm(training_img_links):
        img_data = requests.get(img_link).content
        with open(DATA_FOLDER / train_or_val / os.path.basename(img_link), 'wb') as handler:
            handler.write(img_data)


if __name__ == '__main__':
    if check_or_create_folder(DATA_FOLDER):
        if check_or_create_folder(DATA_FOLDER / 'train'):
            get_images('train')
        if check_or_create_folder(DATA_FOLDER / 'val'):
            get_images('val')
        shutil.copytree(ANNOTATION_FOLDER, DATA_FOLDER / 'annotations')
