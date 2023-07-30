import subprocess


def createLipSyncFile(audioPath, textPath):
    command = f"rhubarb -o ../output.txt {audioPath} -f json -d {textPath} --extendedShapes GHX"

    subprocess.check_output(command.split(' '))

    json_data = {}
    with open('output.txt') as f:
        json_data = json.load(f)

    return json_data["mouthCues"]



