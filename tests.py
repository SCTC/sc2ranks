import unittest
from sc2ranks import *

API_KEY = 'tests@github.com/anrie/sc2ranks'
PLAYER_NAME = 'Kapitulation'
BNET_ID = 316741
REGION = 'eu'
DIVISION_BRACKET = 3
DIVISION_ID = 5404


class BaseTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.client = Sc2Ranks(API_KEY)

    def testConnection(self):
        """Checks if we get a basic response."""
        response = self.client.api_fetch('search/exact/%s/%s' % (REGION, PLAYER_NAME))
        self.assertEqual(response, {u'total': 1, u'characters': [{u'bnet_id': BNET_ID, u'name': PLAYER_NAME}]})

    def testSearchCharacter(self):
        """Search a character by name."""
        response = str(self.client.search_for_character(region=REGION, name=PLAYER_NAME))
        expected = "<Sc2RanksResponse(total=1, characters=[{u'bnet_id': %s, u'name': u'%s'}])>" % (BNET_ID, PLAYER_NAME)
        self.assertEqual(response, expected)

    def testSearchProfile(self):
        """Search a Sc2Ranks-Profile."""
        response = self.client.search_for_profile(region=REGION, name=PLAYER_NAME)[0]
        #do we get a response at all?
        self.assertEqual(type(response), Sc2RanksResponse)
        #check for relevant keys
        self.assertEqual(response.bnet_id, BNET_ID)
        self.assertEqual(response.name, PLAYER_NAME)
        attrs = ['achievement_points', 'team', 'region', 'id']
        for attr in attrs:
            self.assertTrue(hasattr(response, attr))

    def testFetchBaseCharacter(self):
        """Fetch the base data for a character from sc2ranks.com."""
        response = self.client.fetch_base_character(region=REGION, name=PLAYER_NAME, bnet_id=BNET_ID)
        #do we get a response at all?
        self.assertEqual(type(response), Sc2RanksResponse)
        #check for relevant keys
        attrs = ['achievement_points', 'region', 'id', 'updated_at', 'portrait']
        for attr in attrs:
            self.assertTrue(hasattr(response, attr))

    def testFetchBaseCharacterTeams(self):
        """Fetch the base data for a character plus team data from sc2ranks.com."""
        response = self.client.fetch_base_character_teams(region=REGION, name=PLAYER_NAME, bnet_id=BNET_ID)
        #do we get a response at all?
        self.assertEqual(type(response), Sc2RanksResponse)
        #check for relevant keys
        attrs = ['achievement_points', 'region', 'id', 'updated_at', 'portrait', 'teams']
        for attr in attrs:
            self.assertTrue(hasattr(response, attr))

    def testFetchCharacterTeams(self):
        """Fetch the extended team data for a character from sc2ranks.com."""
        response = self.client.fetch_character_teams(region=REGION, name=PLAYER_NAME, bnet_id=BNET_ID, bracket='3v3')
        #do we get a response at all?
        self.assertEqual(type(response), Sc2RanksResponse)
        #check the relevant keys
        attrs = ['achievement_points', 'region', 'id', 'updated_at', 'teams']
        for attr in attrs:
            self.assertTrue(hasattr(response, attr))
        teams = response.teams
        self.assertTrue('3v3' in teams)
        #the two other team-members should be listed
        self.assertEqual(len(teams['3v3'].members), 2)

    def testFetchCustomDivisionCharacters(self):
        """Fetching characters from a custom division."""
        response = self.client.fetch_custom_division_characters(DIVISION_ID, bracket=DIVISION_BRACKET)
        attrs = ['league', 'points', 'division_rank', 'members']
        for team in response:
            for attr in attrs:
                self.assertTrue(hasattr(team, attr))
            self.assertEqual(DIVISION_BRACKET, len(team.members))

    def testSearchNotExistingCharacter(self):
        """Raise an exception if searched character doesn't exist."""
        self.assertRaises(NoSuchCharacterException, self.client.search_for_character, region='eu', name='ThisCharacterDoesNotExistDoesIt')

    def testSearchNotExistingProfile(self):
        """Raise an exception if searched profile doesn't exist."""
        self.assertRaises(NoSuchCharacterException, self.client.search_for_profile, region='eu', name='ThisCharacterDoesNotExistDoesIt')


if __name__ == '__main__':
    unittest.main()
