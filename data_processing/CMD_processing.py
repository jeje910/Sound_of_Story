import os
import sys
import csv

import shutil
import json
import ast

def main(dir_path):
    # CMD paths
    desc_csv_path = './CMD_descriptions.csv'


    dst_dir_path = "./processed_data"
    json_data = []
    all_descriptions = []

    CMD_data = []
    CMD_descriptions = []

    with open("../data/data.jsonl", "r") as file:
        for line in file:
            json_data.append(json.loads(line))
            all_descriptions.append(ast.literal_eval(line)['Desc'].replace("\'", "").replace("\"", ""))


    with open(desc_csv_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i == 0:
                continue
            CMD_data.append(row)
            CMD_descriptions.append(row[2].replace("\'", "").replace("\"", ""))

        
    if not os.path.exists(dst_dir_path):
        os.makedirs(dst_dir_path)


    for i, description in enumerate(CMD_descriptions):
        if description in all_descriptions:
            movie_name = json_data[all_descriptions.index(description)]['Movie']
            CMD_data[i].append(movie_name)
            

    all_CMD_movie_paths = []
    for year in os.listdir(dir_path):
        movie_path = os.path.join(dir_path, year, 'videos')
        for movie_name in sorted(os.listdir(movie_path)):
            all_CMD_movie_paths.append(os.path.join(movie_path, movie_name))



    for data in CMD_data:
        if len(data) == 4:
            matching_indices = [index for index, item in enumerate(all_CMD_movie_paths) if data[1] in item]
            dst_path = os.path.join(dst_dir_path, data[3]+'.avi')
            shutil.copy(all_CMD_movie_paths[matching_indices[0]], dst_path)
            
if __name__ == "__main__":
    dir_path = sys.argv[1]
    main(dir_path)