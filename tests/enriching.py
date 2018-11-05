import sys
from src.enriching import *


def test():
    test_enriched_player_name()
    print('')
    test_players_to_enriching()
    print('')
    print("enricher tests OK")


def test_enriched_player_name():

    # full name provided
    player = {
        'first_name': 'Ann',
        'last_name': 'Boleyn',
        'points_scored': '42'
    }
    s = enriched_player_name(player, 'Cecile Delacroix')
    check(s, 'Cecile Delacroix (p.42)')

    # full name not provided, just first
    player = {
        'first_name': 'Ann',
        'last_name': 'Boleyn',
        'points_scored': '100'
    }
    s = enriched_player_name(player)
    check(s, 'Ann Boleyn (p.100)')

    # full name not provided, having both
    player = {
        'first_name': 'Pele',
        'last_name': None,
        'points_scored': '650'
    }
    s = enriched_player_name(player)
    check(s, 'Pele (p.650)')

    # no points
    player = {
        'first_name': 'John',
        'last_name': 'Doe',
    }
    s = enriched_player_name(player)
    check(s, 'John Doe (p.?)')

    #points None
    player = {
        'first_name': 'Zoe',
        'last_name': 'Zulu',
        'points_scored': None
    }
    s = enriched_player_name(player)
    check(s, 'Zoe Zulu (p.?)')


def test_players_to_enriching():
    player1 = {
        'first_name': 'Alice',
        'last_name': 'Baker',
        'points_scored': '1'
    }
    player2 = {
        'first_name': 'Cindy',
        'points_scored': '2'
    }
    player3 = {
        'last_name': 'Xander',
        'points_scored': '3'
    }
    player4 = {
        'first_name': 'Dan',
        'last_name': 'Elfman',
        'player_code': 'dan_elfman',
        'points_scored': '4'
    }
    player5 = {
        'first_name': 'Felix',
        'last_name': 'Graham',
        'player_code': 'felix_graham',
        'twitter_handle': '@graham',
        'points_scored': '5'
    }
    player6 = {
        'first_name': 'Zoe',
        'last_name': 'Zulu',
        'points_scored': None
    }
    expected = {
        'Alice Baker': 'Alice Baker (p.1)',
        'Baker': 'Alice Baker (p.1)',
        'A.Baker': 'Alice Baker (p.1)',

        'Cindy': 'Cindy (p.2)',

        'Xander': 'Xander (p.3)',

        'Dan Elfman': 'Dan Elfman (p.4)',
        'Elfman': 'Dan Elfman (p.4)',
        'D.Elfman': 'Dan Elfman (p.4)',
        'dan_elfman': 'Dan Elfman (p.4)',

        'Felix Graham': 'Felix Graham (p.5)',
        'Graham': 'Felix Graham (p.5)',
        'F.Graham': 'Felix Graham (p.5)',
        'felix_graham': 'Felix Graham (p.5)',
        '@graham': 'Felix Graham (p.5)',

        'Zoe Zulu': 'Zoe Zulu (p.?)',
        'Zulu': 'Zoe Zulu (p.?)',
        'Z.Zulu': 'Zoe Zulu (p.?)',
    }
    result = players_to_enriching([player1, player2, player3, player4, player5, player6])
    check(expected, result)


def check(a, b, prefix=''):
    assert (a == b), '%s"%s" differs from "%s"' % (prefix, a, b)
    print('.', end='')
    sys.stdout.flush()


if __name__ == '__main__':
    test()