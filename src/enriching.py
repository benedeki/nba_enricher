from .data_layer import PlayerData
def _get_players_last_name_counts(players):
    # type: (list) -> dict
    players_last_names = []
    for player in players:
        players_last_names.append(player['last_name'])
    db = PlayerData()
    return db.last_names_counts(players_last_names)

def player_full_name(player):
    # type: (dict) -> str
    if player.get('last_name', False):
        return ('%s %s' % (player.get('first_name',''), player['last_name'])).strip()
    else:
        return player.get('first_name','').strip()


def players_to_enriching(players):
    # type: (list) -> dict
    last_name_counts = _get_players_last_name_counts(players)
    enriching = dict()
    for player in players:
        full_name = player_full_name(player)
        if player.get('last_name', False):
            last_name = player['last_name']
            if player.get('first_name', False):
                dot_name =  player['first_name'][0] + '.' + last_name
            else:
                dot_name = ''
        else:
            last_name = ''
            dot_name = ''
        # enriched text
        enriched_text = enriched_player_name(player, full_name)
        enriching[full_name] = enriched_text
        if last_name and (last_name_counts.get(last_name, 0) <= 1):
            # Use enriching based on last name only only if it's unique
            enriching[last_name] = enriched_text
        if dot_name:
            enriching[dot_name] = enriched_text
        if player.get('player_code', False):
            enriching[player['player_code']] = enriched_text
        if player.get('twitter_handle', False):
            enriching[player['twitter_handle']] = enriched_text
    return enriching


def enriched_player_name(player, player_full_name=None):
    # type: (dict, str) -> str
    if not player_full_name:
        player_full_name = player_full_name(player)
    points = player.get('points_scored', None)
    if points == None:
        points = '?'
    result = "%s (p.%s)" % (player_full_name, points)
    return result


