import os
import sys
import csv

import shutil
import json
import ast

def main(dir_path):
    # LSMDC directory
    csv_path = dir_path +"/0_Data/annotations/annotation_names/LSMDC16_annos_training.csv"
    csv_path2 = dir_path + "/0_Data/annotations/annotation_names/LSMDC16_annos_val.csv"
    csv_path3 = dir_path + "/0_Data/annotations/annotations_missing_clips.csv"
    csv_path4 = dir_path + "/0_Data/annotations/annotations_missing_clips_test_paraphrase.csv"

    movie_name = os.listdir(dir_path)

    movie_name.remove("downloadVideos.sh")
    movie_name.remove("MPIIMD_downloadLinks.txt")
    movie_name.remove("MVADaligned_downloadLinks.txt")
    movie_name.remove("0_Data")

    # bring description csv
    csv_dict = {}
    with open(csv_path, newline='', encoding='cp932', errors='ignore') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        try:
            for row in spamreader:
                csv_dict[row[0]] = row[5]
        except:
                print("except")

    with open(csv_path2, newline='', encoding='cp932', errors='ignore') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        try:
            for row in spamreader:
                csv_dict[row[0]] = row[5]
        except:
                print("except")

    with open(csv_path3, newline='', encoding='cp932', errors='ignore') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        try:
            for row in spamreader:
                csv_dict[row[0]] = row[1]
        except:
                print("except")

    with open(csv_path4, newline='', encoding='cp932', errors='ignore') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        try:
            for row in spamreader:
                csv_dict[row[0]] = row[6]
        except:
                print("except")

    # print(csv_dict)
    # merge videos with 25 clips
    count = 0
    dst_dir_path = "./processed_data"

    with open("../data/data.jsonl", "r") as file:
        json_data = []
        for line in file:
            json_data.append(json.loads(line))

    if not os.path.exists(dst_dir_path):
        os.makedirs(dst_dir_path)


    for movie in movie_name:
        movie_path = os.path.join(dir_path, movie)
        clips = sorted(os.listdir(movie_path))

        for i, child_movie in enumerate(clips):
            description = csv_dict[child_movie[:-4]]
            
            matching_items = []
            matching_items = [item for item in json_data if description in item["Desc"]]
            for i in range(3):
                if matching_items == []:
                    description = description.replace("\"", "\'")
                    matching_items = [item for item in json_data if description in item["Desc"]]
                else:
                    break
                
                
            for matching_item in matching_items:
                if child_movie[:10] in matching_item['Movie']:
                    if matching_item['Movie']+'.avi' not in os.listdir('./processed_data'):
                        src = os.path.join(dir_path, movie, child_movie)
                        dst = os.path.join(dst_dir_path, matching_item['Movie'] + '.avi')
                        shutil.copy(src, dst)
                    else:
                        base_movie_path = os.path.join(dst_dir_path, matching_item['Movie'] + '.avi')
                        child_movie_path = os.path.join(dir_path, movie, child_movie)
                    
                        concatnate = "\"concat:" + base_movie_path + "|" + child_movie_path + "\""
                        
                        temp_output = matching_item['Movie'] + "_temp.avi"
                        temp_output = os.path.join(dst_dir_path, temp_output)
                        
                        merge_command = "ffmpeg -i "+ concatnate +" -codec copy "+ temp_output
                        print(merge_command)
                        os.system(merge_command)
                        os.rename(temp_output, base_movie_path)

if __name__ == "__main__":
    dir_path = sys.argv[1]
    main(dir_path)