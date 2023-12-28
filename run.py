import asyncio
import logging
import random
from pavlov import PavlovRCON
import player_config  # Assuming you have separated the skins and guns configuration


#PLAYER DATA 
#{player['PlayerName']}?{player['TeamId']}?{player['KDA']}?{player['Ping']}
#76561198210003277: ?Salted ******* Jack?1?0/0/0?44.96428680419922
#        ?ID             ?NAME             ?TEAM ?K/D/A  ?PING 

# Configuration settings
IP = "127.0.0.1"
PORT = 9100
PASSWORD = "RCONPASS"
LOOP_DELAY = 30 # in seconds 300 is 5 mins
RUN_CMD_ON_EACH_LOOP = False  # Or False, as required

# Setting up logging
logging.basicConfig(filename='game_log.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# Dictionary to keep track of players
players_dict = {}

# Asynchronous function to send RCON commands
async def send_command(command):
    pavlov = PavlovRCON(IP, PORT, PASSWORD)
    try:
        response = await pavlov.send(command)
        return response
    finally:
        await pavlov.close()

DEFAULT_SKIN = 'naked'
DEFAULT_GUN = 'bayonet_trenchgun'
DEFAULT_COMMAND = 'slap {unique_id} -50' #removes 50 health

async def inspect_players():
    global players_dict
    response = await send_command("inspectall")
    logging.info(f'InspectAll Response: {response}')

    if response.get('Successful') and response.get('InspectList'):
        for player in response['InspectList']:
            unique_id = player['UniqueId']
            if unique_id in player_config.player_types:
                player_type = player_config.player_types[unique_id]
                skins, gun = player_config.skins_guns[player_type]
                skin = random.choice(skins)  # Randomly select a skin
            else:
                # Default settings for players not in the configuration
                skin = DEFAULT_SKIN
                gun = DEFAULT_GUN



            # Add the player to the players_dict
            if unique_id not in players_dict:
                player_info = f"?{player['PlayerName']}?{player['TeamId']}?{player['KDA']}?{player['Ping']}"
                players_dict[unique_id] = player_info
                logging.info(f'Player Joined: {player_info}')

            # Generate and send commands
            commands = [
                f"GiveItem {unique_id} syringe",
                f"SetPlayerSkin {unique_id} {skin}",
                f"SetCash {unique_id} 100",
                f"GiveItem {unique_id} {gun}"
            ]
            if skin == DEFAULT_SKIN:  # If using default skin, add the slap command
                commands.append(DEFAULT_COMMAND.format(unique_id=unique_id))


            file_path = 'players_data.txt'  # Replace with your desired file path
            try:
                with open(file_path, 'w') as file:
                    for unique_id, player_info in players_dict.items():
                        file.write(f"{unique_id}: {player_info}\n")
            except IOError as e:
                logging.error(f"Error writing to file: {e}")

            for cmd in commands:
                await send_command(cmd)
                logging.info(f'Sent Command: {cmd}')

# Main asynchronous loop
async def main():
    iteration_count = 0
    while True:
        await inspect_players()
        print(f"Sleeping for {LOOP_DELAY} seconds...")
        await asyncio.sleep(LOOP_DELAY)
        iteration_count += 1
        print(f"Iteration: {iteration_count}")

asyncio.run(main())