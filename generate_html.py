import json
from tabulate import tabulate

from datetime import datetime
from os import path, unlink


def detect_mount(character, track_mounts, user_obtained):
    full_list = {}
    for t in track_mounts:
        try:
            full_list[str(t['Name'])] = f"""<a href="https://na.finalfantasyxiv.com/lodestone/character/{character['ID']}/">
            <img src=\"{character['Avatar']}\" width=\"40\" height=\"40\"></a>"""
        except TypeError:
            full_list[t] = ""
            for tr in user_obtained:
                if str(t).lower() == str(tr['Name']).lower():
                    full_list[t] = f"<img src=\"{tr['Icon']}\">"
                    break
    return full_list


def generate_table(gamers, tracking_mounts):
    html = {}
    for raider in gamers:
        html[f"{raider['id']}"] = []
        # print(f"{raider}")

        if int(raider['id']) == 0:
            # Header
            for t in tracking_mounts:
                try:
                    html[f"{raider['id']}"].append(f"<b>{t['Name']}</b>")
                except TypeError:
                    html[f"{raider['id']}"].append(f"{t}")
            continue

        user_data_file = f"characters/{raider['world']}/{raider['forename']}_{raider['surname']}/user.json"
        user = []
        with open(f"{user_data_file}", "r", encoding="utf-8") as file1:
            user = json.load(file1)

        char = user['Character']
        # achieve = user['Achievements']['List']
        # achieve_points = user['Achievements']['Points']
        mounts = user['Mounts']

        char_track_mounts = detect_mount(character=char, track_mounts=tracking_mounts, user_obtained=mounts)
        for mount in char_track_mounts:
            html[f"{raider['id']}"].append(f"{char_track_mounts[mount]}")

    return tabulate(html, tablefmt='unsafehtml')


if __name__ == '__main__':

    html = {}
    html_data = ""
    index = "index.html"
    if path.exists(index):
        unlink(index)

    with open("gamers.json", "r", encoding="utf-8") as file1:
        raider_list = json.load(file1)

    mount_file = [
        "data/mounts/arr.json",
        "data/mounts/heavensward.json",
        "data/mounts/stormblood.json",
        "data/mounts/shadowbringers.json",
        "data/mounts/endwalker.json",
        "data/mounts/tanks.json",
        "data/mounts/vendor.json",
        "data/mounts/pvp.json",
        "data/mounts/other.json",
        "data/mounts/skybuilders.json",
        "data/mounts/bozja.json"
    ]
    extra_mount_file = "data/download.json"
    if path.exists(extra_mount_file):
        with open(extra_mount_file, "r", encoding="utf-8") as file1:
            extra_mounts = json.load(file1)

        extra_map = []
        res = []
        # extra_map.append({"Name": "Extra", "Logo": ""})
        for data in extra_mounts['results']:
            extra_map.append(str(data['name']).strip())
        extra_map.sort()
        extra_map.insert(0, {"Name": "Extra", "Logo": ""})

    for tracking_mounts in mount_file:
        print(f"{tracking_mounts}")
        with open(tracking_mounts, "r", encoding="utf-8") as file1:
            tracker = json.load(file1)

        try:
            count = 0
            for ex in extra_map:
                for track in tracker:
                    if str(ex).lower().replace(" ", "").strip() == str(track).lower().replace(" ", "").strip():
                        print(f"Duplicate {ex}")
                        del extra_map[count]
                count += 1
        except:
            extra_map=[]

        if tracker[0]['Logo']:
            if str(tracker[0]['Logo'][-4:]).lower() == '.png':
                html_data += f"<img src=\"{tracker[0]['Logo']}\" width=\"40\" height=\"40\" >"
        html_data += generate_table(gamers=raider_list, tracking_mounts=tracker) + "<br><br>"

    if extra_map:
        # GET https://ffxivcollect.com/api/mounts/
        print("Generate Extra from download.json")
        html_data += generate_table(gamers=raider_list, tracking_mounts=extra_map) + "<br><br>"

    with open(index, "w+", encoding="utf-8") as file1:
        file1.write(f"""<!DOCTYPE html>
<style type="text/css">
    table, th, td {{
        border: 1px solid black;
        border-collapse: collapse;
        height: 47px;
    }}
    td img {{
        padding: 2px;
        display: block;
    }}
</style>
<html>

Last Updated: {datetime.utcnow().strftime("%Y/%m/%d @%H:%M:%S")} UTC
<hr>
<h1>This site is only for friends of Shinobu!</h1>
<body>
{html_data}
</body></html>
""")
