#!/usr/bin/env python3

import argparse
import json
import re
from datetime import datetime
from os import path, unlink

from tabulate import tabulate


def equal(a, b):
    # Ignore non-space and non-word characters
    regex = re.compile(r"[^\s\w]")
    return regex.sub("", a).lower() == regex.sub("", b).lower()


def detect_mount_json(
    track_mounts,
    user_obtained,
):
    full_list = {}
    for t in track_mounts:
        full_list[t] = ""
        for tr in user_obtained:
            if equal(
                str(t),
                str(tr["Name"]),
            ):
                full_list[t] = f"<img src=\"{tr['Icon']}\">"
                user_obtained.remove(tr)
                break
    return full_list


def detect_achievments(user, tracking):
    full_list = {}
    for t in tracking:
        full_list[t] = ""
        for tr in user:
            if equal(
                str(t),
                str(tr["Name"]),
            ):
                full_list[t] = f"<img src=\"https://xivapi.com/{tr['Icon']}\">"
                user.remove(tr)
                break
    return full_list


def generate_table_json(gamers, tracking):
    html = {}
    for raider in gamers:
        html[f"{raider['id']}"] = []
        # print(f"{raider}")

        if int(raider["id"]) == 0:
            # Header
            html[f"{raider['id']}"].append(f"<b>{tracking['meta']['Name']}</b>")

            if "ClassJobsBozjan" in tracking:
                html[f"{raider['id']}"].append("Resistance Rank")

            if "ClassJobsElemental" in tracking:
                html[f"{raider['id']}"].append("Elemental Level")

            if "BLU" in tracking:
                html[f"{raider['id']}"].append("🪄")

            if "mounts" in tracking:
                for t in tracking["mounts"]:
                    html[f"{raider['id']}"].append(f"🏇{t}")

            if "minions" in tracking:
                for t in tracking["minions"]:
                    html[f"{raider['id']}"].append(f"🐈{t}")

            if "AchievementPoints" in tracking:
                html[f"{raider['id']}"].append("⭐Points")

            if "achivements" in tracking:
                for t in tracking["achivements"]:
                    html[f"{raider['id']}"].append(f"⭐{t}")
            continue

        user_data_file = f"characters/{raider['world']}/{raider['forename']}_{raider['surname']}/user.json"
        user = []
        with open(
            f"{user_data_file}",
            "r",
            encoding="utf-8",
        ) as file1:
            user = json.load(file1)

        char = user["Character"]
        achieve = user["Achievements"]["List"]
        classes = char["ClassJobs"]

        html[f"{raider['id']}"].append(
            f"""<a href="https://na.finalfantasyxiv.com/lodestone/character/{char['ID']}/">
            <img src=\"{char['Avatar']}\" width=\"40\" height=\"40\"></a>"""
        )

        if "ClassJobsBozjan" in tracking:
            bozja = char["ClassJobsBozjan"]
            if bozja["Level"] is None:
                bozja["Level"] = ""

            html[f"{raider['id']}"].append(f"{bozja['Level']}")

        if "ClassJobsElemental" in tracking:
            eureka = char["ClassJobsElemental"]
            if eureka["Level"] is None:
                eureka["Level"] = ""
            html[f"{raider['id']}"].append(f"{eureka['Level']}")

        if "BLU" in tracking:
            for job in classes:
                if job["Class"]["Abbreviation"] == "BLU":
                    blu = job
                    if blu["Level"] != 0:
                        html[f"{raider['id']}"].append(f"{blu['Level']}")
                    else:
                        html[f"{raider['id']}"].append("")

        if "mounts" in tracking:
            mounts = user["Mounts"]
            mount_table = detect_mount_json(
                track_mounts=tracking["mounts"],
                user_obtained=mounts,
            )
            for t in mount_table:
                html[f"{raider['id']}"].append(f"{mount_table[t]}")

        if "minions" in tracking:
            mounts = user["Minions"]
            minion_table = detect_mount_json(
                track_mounts=tracking["minions"],
                user_obtained=mounts,
            )
            for t in minion_table:
                html[f"{raider['id']}"].append(f"{minion_table[t]}")

        if "AchievementPoints" in tracking:
            if user["Achievements"]["Points"] != 0:
                html[f"{raider['id']}"].append(f"{user['Achievements']['Points']}")
            else:
                html[f"{raider['id']}"].append("")

        if "achivements" in tracking:
            set_acheivement_table = detect_achievments(
                user=achieve,
                tracking=tracking["achivements"],
            )
            for table in set_acheivement_table:
                html[f"{raider['id']}"].append(f"{set_acheivement_table[table]}")

    return tabulate(
        html,
        tablefmt="unsafehtml",
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--gamer_data",
        help="List of gamers in gamers.json, keep the 1st line for header",
        default="gamers.json",
    )
    parser.add_argument(
        "--website",
        help="List of gamers in gamers.json, keep the 1st line for header",
        default="index.html",
    )
    args = parser.parse_args()

    html = {}
    html_data = ""
    index = args.website
    if path.exists(index):
        unlink(index)

    with open(
        args.gamer_data,
        "r",
        encoding="utf-8",
    ) as file1:
        raider_list = json.load(file1)

    mount_file = [
        "data/arr.json",
        "data/heavensward.json",
        "data/stormblood.json",
        "data/shadowbringers.json",
        "data/endwalker.json",
        "data/tanks.json",
        "data/vendor.json",
        "data/pvp.json",
        "data/other.json",
        "data/skybuilders.json",
        "data/bozja.json",
        "data/blumage.json",
    ]
    extra_mount_file = "data/download.json"
    if path.exists(extra_mount_file):
        with open(
            extra_mount_file,
            "r",
            encoding="utf-8",
        ) as file1:
            extra_mounts = json.load(file1)

        extra_map = []
        res = []
        # extra_map.append({"Name": "Extra", "Logo": ""})
        for data in extra_mounts["results"]:
            extra_map.append(str(data["name"]).strip())
        extra_map.sort()
        extra_map.insert(
            0,
            {
                "Name": "Extra",
                "Logo": "",
            },
        )

    for tracking_mounts in mount_file:
        print(f"{tracking_mounts}")
        with open(
            tracking_mounts,
            "r",
            encoding="utf-8",
        ) as file1:
            tracker = json.load(file1)

        if tracker["meta"]["Logo"]:
            if str(tracker["meta"]["Logo"][-4:]).lower() == ".png":
                html_data += f"<img src=\"{tracker['meta']['Logo']}\" width=\"40\" height=\"40\" >"
        html_data += (
            generate_table_json(
                gamers=raider_list,
                tracking=tracker,
            )
            + "<br><br>"
        )

    with open(
        index,
        "w+",
        encoding="utf-8",
    ) as file1:
        file1.write(
            f"""<!DOCTYPE html>
    <link rel="stylesheet" href="ffxiv.css" type="text/css">
<html>
<head>
<meta charset = "utf-8" />
<title>Shinobu's Basement</title>
<link rel = "icon" href = "https://xivapi.com/img-misc/mappy/aetheryte_small.png" type = "image/x-icon">
</head>
Last Updated: {datetime.utcnow().strftime("%Y/%m/%d @%H:%M:%S")} UTC
<hr>
<h1>This site is only for friends of Shinobu!</h1>
<body>
{html_data}
</body></html>
"""
        )
