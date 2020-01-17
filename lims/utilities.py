import os
import json

PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))
FILE_CONFIG = "file_conf.json"


def generate_directories(workflow_name):
    data_path = os.path.join(PROJECT_PATH, "app-data")
    workflow_path = os.path.join(data_path, workflow_name)
    source_path = os.path.join(workflow_path, "src")
    output_path = os.path.join(workflow_path, "output")
    if not os.path.exists(workflow_path):
        os.mkdir(workflow_path)
        if not os.path.exists(source_path):
            os.mkdir(source_path)
        if not os.path.exists(output_path):
            os.mkdir(output_path)
    return source_path, output_path


def update_file_config(id, name, src, out, v_src, v_out):
    data_path = os.path.join(PROJECT_PATH, "app-data")
    file_config_path = os.path.join(data_path, FILE_CONFIG)
    new_config = {
        "id": id,
        "name": name,
        "source": src,
        "dest": out,
        "v_source": v_src,
        "v_dest": v_out
    }
    with open(file_config_path, 'r') as j_file:
        configs = json.load(j_file)
    is_new = True
    for c in configs["workflows"]:
        if c.id == id:
            is_new = False
    if is_new:
        configs["workflows"].append(new_config)
    with open(file_config_path, 'w') as j_file:
        json.dump(configs, j_file)
