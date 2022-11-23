import sys
sys.path.append("..")
import main
import os


def show_files(path, all_files):
    file_list = os.listdir(path)
    for file in file_list:
        cur_path = os.path.join(path, file)
        if os.path.isdir(cur_path):
            show_files(cur_path, all_files)
        else:
            all_files.append(file)

    return all_files


contents = show_files("./in", [])

for content in contents:
    main.testOutput("./in/%s"%content)