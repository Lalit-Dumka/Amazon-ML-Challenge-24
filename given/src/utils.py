import re
import constants
import os
import requests
import pandas as pd
import multiprocessing
import time
from time import time as timer
from tqdm import tqdm
import numpy as np
from pathlib import Path
from functools import partial
import requests
import urllib
from PIL import Image

def common_mistake(unit):
    if unit in constants.allowed_units:
        return unit
    if unit.replace('ter', 'tre') in constants.allowed_units:
        return unit.replace('ter', 'tre')
    if unit.replace('feet', 'foot') in constants.allowed_units:
        return unit.replace('feet', 'foot')
    return unit

def parse_string(s):
    s_stripped = "" if s==None or str(s)=='nan' else s.strip()
    if s_stripped == "":
        return None, None
    pattern = re.compile(r'^-?\d+(\.\d+)?\s+[a-zA-Z\s]+$')
    if not pattern.match(s_stripped):
        raise ValueError("Invalid format in {}".format(s))
    parts = s_stripped.split(maxsplit=1)
    number = float(parts[0])
    unit = common_mistake(parts[1])
    if unit not in constants.allowed_units:
        raise ValueError("Invalid unit [{}] found in {}. Allowed units: {}".format(
            unit, s, constants.allowed_units))
    return number, unit


def create_placeholder_image(image_save_path):
    try:
        placeholder_image = Image.new('RGB', (100, 100), color='black')
        placeholder_image.save(image_save_path)
    except Exception as e:
        return

def download_image(image_link, save_folder, retries=3, delay=3):
    if not isinstance(image_link, str):
        return

    filename = Path(image_link).name
    image_save_path = os.path.join(save_folder, filename)

    if os.path.exists(image_save_path):
        return filename

    for _ in range(retries):
        try:
            urllib.request.urlretrieve(image_link, image_save_path)
            return
        except:
            time.sleep(delay)

    print("Failed to download image: {}".format(image_link))    
    create_placeholder_image(image_save_path) #Create a black placeholder image for invalid links/images

def download_images(image_links, download_folder, allow_multiprocessing=True):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    if allow_multiprocessing:
        download_image_partial = partial(
            download_image, save_folder=download_folder, retries=3, delay=3)

        with multiprocessing.Pool(16) as pool:
            list(tqdm(pool.imap(download_image_partial, image_links), total=len(image_links)))
            pool.close()
            pool.join()
    else:
        for image_link in tqdm(image_links, total=len(image_links)):
            download_image(image_link, save_folder=download_folder, retries=3, delay=3)
        

#download all the images from csv
def download_images_from_csv(csv_path, download_folder):
    df = pd.read_csv(csv_path)
    image_links = df['image_link']
    # print("Downloading images from {} to {}".format(csv_path, download_folder))
    download_images(image_links, download_folder)


# def download_images_from_csv(csv_path, download_folder):
#     df = pd.read_csv(csv_path)
#     for img in df['image_link']:
#         df[img]=download_image(img, download_folder)
#     df.to_csv("img_train.csv")
if __name__ == "__main__":
    download_images_from_csv(r'D:\ML\amazon_ml_2024\student_resource\dataset\train.csv', r'D:\ML\amazon_ml_2024\student_resource\dataset\images\train')


    # 75000

    """
Failed to download image: https://m.media-amazon.com/images/I/DzP2RMRQO0.jpg
Failed to download image: https://m.media-amazon.com/images/I/71T2DuimMhL.jpg
Failed to download image: https://m.media-amazon.com/images/I/71HXCZPczsL.jpg
Failed to download image: https://m.media-amazon.com/images/I/lwd2cSmT2ux.jpg
Failed to download image: https://m.media-amazon.com/images/I/VCEdbX8DT28.jpg
Failed to download image: https://m.media-amazon.com/images/I/J2DXsUjR8ay.jpg
Failed to download image: https://m.media-amazon.com/images/I/61uYoWEo7wL.jpg
Failed to download image: https://m.media-amazon.com/images/I/61sJw5WtL7L.jpg
Failed to download image: https://m.media-amazon.com/images/I/51QRnbIcRDL.jpg
Failed to download image: https://m.media-amazon.com/images/I/61-uOjbWH8L.jpg
Failed to download image: https://m.media-amazon.com/images/I/81BDPf4fpbL.jpg
Failed to download image: https://m.media-amazon.com/images/I/71921CxSjaL.jpg
Failed to download image: https://m.media-amazon.com/images/I/71x9hFyrEJL.jpg
Failed to download image: https://m.media-amazon.com/images/I/81h1t-PNnWL.jpg
Failed to download image: https://m.media-amazon.com/images/I/715vNCFQHBL.jpg
Failed to download image: https://m.media-amazon.com/images/I/71aRWIN3oGL.jpg
Failed to download image: https://m.media-amazon.com/images/I/7181tlqDErS.jpg
Failed to download image: https://m.media-amazon.com/images/I/81FtWlKhyeL.jpg
Failed to download image: https://m.media-amazon.com/images/I/81Jom61qKwL.jpg
Failed to download image: https://m.media-amazon.com/images/I/61xlILsuRWS.jpg
Failed to download image: https://m.media-amazon.com/images/I/71LWjRsYHKL.jpg
Failed to download image: https://m.media-amazon.com/images/I/51L5JhTHU9L.jpg
Failed to download image: https://m.media-amazon.com/images/I/RBE3EPzT4OZ.jpg
Failed to download image: https://m.media-amazon.com/images/I/fUyC7fnSnys.jpg
Failed to download image: https://m.media-amazon.com/images/I/61hzAXKuRWL.jpg
Failed to download image: https://m.media-amazon.com/images/I/61W19veGzGL.jpg
Failed to download image: https://m.media-amazon.com/images/I/81N8v9BYVoL.jpg
Failed to download image: https://m.media-amazon.com/images/I/61J2svB246L.jpg
Failed to download image: https://m.media-amazon.com/images/I/71luZkTFRUL.jpg
Failed to download image: https://m.media-amazon.com/images/I/51tDb-KpK0L.jpg
Failed to download image: https://m.media-amazon.com/images/I/71ecSbXM-ES.jpg
Failed to download image: https://m.media-amazon.com/images/I/81ZjExo2oFL.jpg
Failed to download image: https://m.media-amazon.com/images/I/810ZqD7S7bL.jpg
ailed to download image: https://m.media-amazon.com/images/I/9BIu8SYSAek.jpg
 15%|██████████████▊                                                                                   | 39946/263859 [3:03:31<31:33:21,  1.97it/s]Failed to download image: https://m.media-amazon.com/images/I/T8hQGdjTcGp.jpg
 18%|█████████████████▉                                                                                | 48365/263859 [3:27:53<10:03:47,  5.95it/s]Failed to download image: https://m.media-amazon.com/images/I/mWyQ79S76i.jpg
 22%|██████████████████████                                                                            | 59247/263859 [4:00:18<11:44:33,  4.84it/s]Failed to download image: https://m.media-amazon.com/images/I/71zNLbSeS5L.jpg
Failed to download image: https://m.media-amazon.com/images/I/61WMBJeD1+S.jpg
Failed to download image: https://m.media-amazon.com/images/I/61-DxyDGr9L.jpg
Failed to download image: https://m.media-amazon.com/images/I/61AQEiso4rL.jpg
 22%|██████████████████████                                                                            | 59248/263859 [4:00:34<83:50:53,  1.48s/it]Failed to download image: https://m.media-amazon.com/images/I/81R39Np1-gL.jpg
Failed to download image: https://m.media-amazon.com/images/I/61bfINbD-eL.jpg
Failed to download image: https://m.media-amazon.com/images/I/61k-mRsTITL.jpg
Failed to download image: https://m.media-amazon.com/images/I/61Xyi1sRwCL.jpg
Failed to download image: https://m.media-amazon.com/images/I/71zDkuRbAwL.jpg
Failed to download image: https://m.media-amazon.com/images/I/71OnNsqZtXL.jpg
Failed to download image: https://m.media-amazon.com/images/I/71BQ7P2NNqL.jpg
Failed to download image: https://m.media-amazon.com/images/I/71zDkuRbAwL.jpg
Failed to download image: https://m.media-amazon.com/images/I/51OSe1VgksL.jpg
Failed to download image: https://m.media-amazon.com/images/I/71qd2DzQREL.jpg
Failed to download image: https://m.media-amazon.com/images/I/915MaQnD6oL.jpg
Failed to download image: https://m.media-amazon.com/images/I/71nMfhDw+fL.jpg
ailed to download image: https://m.media-amazon.com/images/I/H8fMd0pRI6n.jpg
 25%|████████████████████████▎                                                                         | 65395/263859 [4:30:00<13:19:36,  4.14it/s]Failed to download image: https://m.media-amazon.com/images/I/VjCkaPeR1o.jpg
 25%|████████████████████████▋                                                                         | 66480/263859 [4:36:20<19:29:08,  2.81it/s]Failed to download image: https://m.media-amazon.com/images/I/l8BsJVaKRCe.jpg
Failed to download image: https://m.media-amazon.com/images/I/71OoA8hZNPL.jpg
Failed to download image: https://m.media-amazon.com/images/I/71O1CqVI5jL.jpg
 25%|███████████████████████▍                                                                     | 66489/263859 [10:29:56<36829:50:24, 671.77s/it]Failed to download image: https://m.media-amazon.com/images/I/71t60mEcJKL.jpg
Failed to download image: https://m.media-amazon.com/images/I/71HUAqY3RtL.jpg
Failed to download image: https://m.media-amazon.com/images/I/71Vlaa08lQL.jpg
Failed to download image: https://m.media-amazon.com/images/I/91qNCt+rGoL.jpg
Failed to download image: https://m.media-amazon.com/images/I/51-dH-8NiLL.jpg
 35%|█████████████████████████████████▉                                                               | 92221/263859 [10:29:59<27:31:45,  1.73it/s]Failed to download image: https://m.media-amazon.com/images/I/61aK2fBlZpL.jpg
 ailed to download image: https://m.media-amazon.com/images/I/PBWKX4CRl2o.jpg
Failed to download image: https://m.media-amazon.com/images/I/3sSrJnc5R58.jpg
Failed to download image: https://m.media-amazon.com/images/I/81-zDlxYl9L.jpg
Failed to download image: https://m.media-amazon.com/images/I/91u9n5yDXXL.jpg
Failed to download image: https://m.media-amazon.com/images/I/81iU9CvtrQL.jpg
    """