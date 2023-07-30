import subprocess
import json
import os
import uuid

def create_lip_sync_file(audio_path, text: str):
    file_path = "lipsync.txt"

    with open(f"{file_path}", "w") as f:
        f.write(text)
        f.close()
    command = f"{os.path.abspath(os.getcwd())}/app/api/core/lipsyncing/lipsyncer/rhubarb -o output.txt {audio_path} -f json -d {file_path} --extendedShapes GHX"

    subprocess.check_output(command.split(' '))

    with open('output.txt') as f:
        json_data = json.load(f)
        print(json_data)
        return json_data["mouthCues"]





