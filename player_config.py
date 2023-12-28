# player_config.py

# Skins and guns mappings based on player types
skins_guns = {
    1: (['russian4', 'russian3', 'russian2'], 'tokarev'),
    2: (['nato1', 'nato2', 'nato3'], '1911'),
    3: (['aurora'], 'smg')
}

# Example mapping of unique_id to a number (1-3)
player_types = {
    '76561190210003277': 1,
    # ... other players ...
}

# COMMAND_TEMPLATES definition
COMMAND_TEMPLATES = ["GiveItem {unique_id} syringe", "SetPlayerSkin {unique_id} {skin}", "SetCash {unique_id} 100", "GiveItem {unique_id} {gun}"]
