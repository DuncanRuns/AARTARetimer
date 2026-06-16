import json
import sys
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def play_log_reader(file_path):
    with open(file_path, "r") as f:
        while 1:
            l = f.readline()
            if l:
                yield l
            else:
                return


def format_time(millis: int):
    # returns str h:mm:ss.mmm
    total_seconds = millis / 1000
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = total_seconds % 60
    return f"{hours}:{minutes:02d}:{seconds:06.3f}"


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        Tk().withdraw()
        file_path = askopenfilename(title="Select world's play.log")
        if not file_path:
            print("No file selected")
            sys.exit(1)

    r = play_log_reader(file_path)

    advancements = set()
    start_time = -1

    while 1:
        line = next(r, None)
        if not line:
            break
        j: dict = json.loads(line)
        # Example: {"time":1781562444029,"type":"advancement","data":{"player":{"name":"Jaykeycakey01","uuid":"0d871103-7f2b-4ead-bbd0-f084de514c62"},"id":"minecraft:story/mine_stone","criterion_name":"get_stone","completed":true,"display":{"hidden":false,"announce_to_chat":true,"show_toast":true}},"speedrunigt":{"rta":38178,"igt":38178,"retime":38178}}

        if start_time == -1 and j['type'] == 'game_info' and len(j['data']['players']) > 0:
            start_time = j['time']
        elif j['type'] == 'advancement' and j['data']['completed'] and j['data']['display']:
            aid = j['data']['id']
            if aid in advancements:
                continue
            advancements.add(aid)
            player = j['data']['player']['name']
            if start_time == -1:
                print(
                    f"Advancement #{len(advancements)} {aid} completed before time started by {player}")
            else:
                total_time = j['time'] - start_time
                print(
                    f"Advancement #{len(advancements)} {aid} completed at {format_time(total_time)} by {player}")
