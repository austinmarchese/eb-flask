import unittest
from src.main.utils.banter_dictionary_creator.create_player_dict import get_position
import os
from os.path import dirname, realpath
from src.main.utils.nlp_resource_util import NLPResourceUtil

BASEDIR = os.path.abspath(os.path.dirname(dirname(dirname(realpath(__file__)))))

class Player():
    def __init__(self, position, player_id=None):
        self._position = position
        self.player_id = player_id

class PlayerNoPosition():
    def __init__(self):
        pass


class TestCreatePlayerDict(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.util = NLPResourceUtil()
        FIXTURE_LOCATION = '%s/resources/fixtures' % BASEDIR
        self.integration_test_fixture = self.util.read_json_file(FIXTURE_LOCATION,
                                                                               "create_player_dict_position_fixture.json")

    # @unittest.skip("Skip when testing locally, this is a full integration test, uncomment in production")
    def test_get_sports_tags_normalized_text_test(self):
        for (player_id, position_and_response) in self.integration_test_fixture.items():
            player = Player(position_and_response['position'], player_id)
            position = get_position(player, 'NFL')
            print(player_id, position_and_response, position)
            self.assertCountEqual(position, position_and_response['response'])

    def test_get_position_ss(self):
        player = Player(['SS', '2B', 'RF'])
        position = get_position(player, 'MLB')
        self.assertEqual(position, 'SS')

    def test_get_position_of(self):
        player = Player(['CF', 'OF', 'RF'])
        position = get_position(player, 'MLB')
        self.assertEqual(position, 'OF')

    def test_get_position_outfield_not_main_position(self):
        player = Player(['1B', 'OF', 'RF'])
        position = get_position(player, 'MLB')
        self.assertEqual(position, '1B')

    def test_get_position_bball(self):
        player = Player('PG')
        position = get_position(player, 'NBA')
        self.assertEqual(position, 'PG')

    def test_get_position_football(self):
        player = Player('QB/RB/DT')
        position = get_position(player, 'NFL')
        self.assertEqual(position, 'QB')

    def test_get_position_NFL_non_fantasy(self):
        player = Player('DT')
        position = get_position(player, 'NFL')
        self.assertEqual(position, '')

    def test_get_position_NFL_after_empty(self):
        player = Player(['', 'RB', ''])
        position = get_position(player, 'NFL')
        self.assertEqual(position, 'RB')

    def test_get_position_NFL_after_empty_non_fantasy_position(self):
        player = Player(['', 'DT', ''])
        position = get_position(player, 'NFL')
        self.assertEqual(position, '')

    def test_get_position_no_position(self):
        player = PlayerNoPosition()
        position = get_position(player, 'MLB')
        self.assertEqual(position, '')



if __name__ == '__main__':
    unittest.main()
