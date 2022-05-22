import asyncio
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
    api_key = ""
    with open("gamers.json", "r") as file1:
        raider_list = json.load(file1)
        del raider_list[0]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_example_results(client_api=api_key, raider_list=raider_list))
