"""Script that executes all other scripts in this repository
"""
from scraping.generate_data import generate_data
from scraping.generate_data import generate_reddit_ids_json
from scraping.generate_data import generate_reddit_json
from scraping.generate_data import read_objs
from models.build_model import build_model 
import json
import time
from datetime import datetime

def main():
    NEW_DATA = 0
    GEN_DATA = 0
    GEN_REDDIT_IDS = 1
    GEN_REDDIT_OBJS = 1
    BUILD = 0
    # allows for user to choose variables for data collection, may yield better
    # results in the future

    if GEN_REDDIT_IDS:
        now = datetime.utcnow().strftime("%Y-%m-%d_%H:%M:%S")
        id_file = generate_reddit_ids_json(now)
        print(id_file)
    if GEN_REDDIT_OBJS:
        obj_file = generate_reddit_json(id_file)
        print("file writting, going to read")
        time.sleep(1)
        read_objs(obj_file)
    if GEN_DATA:
        generate_data(50, 10, 10)
    if BUILD:
        print("building model...")
        build_model(file_name)

if __name__ == '__main__':
    main()
