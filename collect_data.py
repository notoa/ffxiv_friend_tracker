#!/usr/bin/env python3

import asyncio
import argparse
import logging

import os
import json

import pyxivapi


async def fetch_example_results(client_api, raider_list):
    client = pyxivapi.XIVAPIClient(
        api_key=str(client_api)
    )

    for raider in raider_list:
        print(f"{raider}")
        save_world_folder = f"characters/{raider['world']}/{raider['forename']}_{raider['surname']}"
        if not os.path.exists(save_world_folder):
            os.makedirs(save_world_folder)

        character = await client.character_by_id(
            lodestone_id=raider['id'],
            extended=True,
            include_freecompany=False,
            include_achievements=True,
            include_minions_mounts=True,
            include_classjobs=False
        )

        with open(f"{save_world_folder}/user.json", "w") as file1:
            file1.write(json.dumps(character, sort_keys=True, indent=4))

    await client.session.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='%H:%M')
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--api_key',
        '-key',
        required=True
    )
    parser.add_argument(
        '--gamer_data',
        help="List of gamers in gamers.json, keep the 1st line for header",
        default="gamers.json"
    )
    args = parser.parse_args()

    with open(args.gamer_data, "r") as file1:
        raider_list = json.load(file1)
        del raider_list[0]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_example_results(client_api=args.api_key, raider_list=raider_list))
