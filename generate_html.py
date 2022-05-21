import json
from tabulate import tabulate

from datetime import datetime


def detect_mount(track_mounts, website_mounts):
    full_list = {}
    for t in track_mounts:
        try:
            full_list[str(t['Name'])] = f"<img src=\"{t['Logo']}\" width=\"40\" height=\"40\">"
        except TypeError:
            full_list[t] = ""
            for tr in website_mounts:
                if str(t).lower() == str(tr['Name']).lower():
                    full_list[t] = f"<img src=\"{tr['Icon']}\">"
                    break

    return full_list


if __name__ == '__main__':

    raider_list = []
    html = {}
    with open("raiders.json", "r") as file1:
        raider_list = json.load(file1)

    other_mounts = [
        {
            "Name": "Other",
            "Logo": "images/logos/other.png"
        },
        "Amaro",
        "Warlion",
        "Battle Lion",

        "Warbear",
        "Battle Bear",

        "War Panther",
        "Battle Panther",

        "War Tiger",
        "Battle Tiger",

        "Black Pegasus",
        "Magitek Avenger",
        "Magitek Avenger A-1",
        "Tyrannosaur",
        "Rathalos",
        "Eldthurs",
        "Demi-Ozma",
        "Triceratops",
        "Construct 14",
        "Cerberus",
        "Gabriel Mark III",
        "Al-iklil",
        "Lunar Whale",
        "Magicked Card"
    ]
    arr_mounts = [
        {
            "Name": "Realm Reborn",
            "Logo": "images/logos/arr.png"
        },
        "Company Chocobo",

        "Nightmare",
        "Aithon",
        "Xanthos",
        "Gullfaxi",
        "Enbarr",
        "Markab",
        "Boreas",
        "Kirin",

        "Logistics System"
    ]

    heaven_mounts = [
        {
            "Name": "Heaven's Ward",
            "Logo": "images/logos/heavens.png"
        },
        "Griffin",
        "Wyvern",

        "White Lanner",
        "Rose Lanner",
        "Round Lanner",
        "Warring Lanner",
        "Dark Lanner",
        "Sophic Lanner",
        "Demonic Lanner",
        "Firebird",

        "Gobwalker",
        "Arrhidaeus",
    ]

    storm_blood_mount = [
        {
            "Name": "Stormblood",
            "Logo": "images/logos/stormblood.png"
        },
        "Syldra",
        "Ixion",

        "Blissful Kamuy",
        "Reveling Kamuy",
        "Legendary Kamuy",
        "Auspicious Kamuy",
        "Lunar Kamuy",
        "Euphonious Kamuy",
        "Hallowed Kamuy",
        "Kamuy Of The Nine Tails",

        "Alte Roite",
        "Air Force",
        "Model O"
    ]
    shadowbringers_mount = [
        {
            "Name": "Shadowbringers",
            "Logo": "images/logos/shadow.png"
        },
        "Fae Gwiber",
        "Innocent Gwiber",
        "Shadow Gwiber",
        "Gwiber Of Light",
        "Ruby Gwiber",
        "Emerald Gwiber",
        "Diamond Gwiber",
        "Landerwaffe",

        "Skyslipper",
        "Ramuh",
        "Eden"
    ]
    endwalker_mounts = [
        {
            "Name": "Endwalker",
            "Logo": "images/logos/endwalker.png"
        },
        "Lynx Of Eternal Darkness",
        "Lynx Of Divine Light",
        "Bluefeather Lynx",
        "Demi-Phoinix"
    ]
    track_raid_achievments = [
        2591,
        2443,
        3035,
        3038
    ]

    full_mount_list = (
        arr_mounts +
        heaven_mounts +
        storm_blood_mount +
        shadowbringers_mount +
        endwalker_mounts +
        other_mounts
    )

    for raider in raider_list:
        html[f"{raider['id']}"] = []
        print(f"{raider}")

        if int(raider['id']) == 0:
            # Header
            html[f"{raider['id']}"].append("")
            for t in full_mount_list:
                try:
                    html[f"{raider['id']}"].append(f"<b>{t['Name']}</b>")
                except TypeError:
                    html[f"{raider['id']}"].append(f"{t}")
            continue

        user_data_file = f"characters/{raider['world']}/{raider['forename']}_{raider['surname']}/user.json"
        user = []
        with open(f"{user_data_file}", "r") as file1:
            user = json.load(file1)

        char = user['Character']
        achieve = user['Achievements']['List']
        achieve_points = user['Achievements']['Points']
        mounts = user['Mounts']

        # print(f"{char['Name']}")
        fake_name = f"{raider['forename'][0]}.{raider['surname'][0]}"
        html[f"{raider['id']}"].append(
            f"""<a href="https://na.finalfantasyxiv.com/lodestone/character/{raider['id']}/">
            <img src=\"{char['Avatar']}\" width=\"40\" height=\"40\"></a><br>{fake_name}""")

        char_track_mounts = detect_mount(full_mount_list, mounts)
        for mount in char_track_mounts:
            html[f"{raider['id']}"].append(f"{char_track_mounts[mount]}")

    now = datetime.utcnow()

    current_time = now.strftime("%Y/%m/%d @%H:%M:%S")
    with open("index.html", "w") as file1:
        file1.write("""<!DOCTYPE html>
<style type="text/css">
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
    }
</style>

<html>
<h1>This site is only for friends of Shinobu!</h1>
<body>
""" + tabulate(html, tablefmt='unsafehtml') + f"""
<hr>
Last Updated: {current_time} UTC
</body>
</html>
"""
        )
