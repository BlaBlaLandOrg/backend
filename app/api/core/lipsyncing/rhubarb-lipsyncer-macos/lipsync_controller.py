import subprocess
import json

def createLipSyncFile(audioPath, textPath):


    command = f"rhubarb -o output.txt sam.wav -f json --extendedShapes GHX"
    #command = f"rhubarb -o ../output.txt {audioPath} -f json -d {textPath} --extendedShapes GHX"

    subprocess.check_output(command.split(' '))

    json_data = {}
    with open('output.txt') as f:
        json_data = json.load(f)

    return json_data["mouthCues"]




if __name__ == '__main__':
    createLipSyncFile("test", "test")

