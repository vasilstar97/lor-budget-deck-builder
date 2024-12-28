import requests
import pandas as pd
from typing import Literal
from .const import LOR_GG_URL, MASTERING_RUNETERRA_URL
from .models.rarity import Rarity

class Parser():

    def __init__(self, lor_gg_url : str = LOR_GG_URL, mastering_runeterra_url : str = MASTERING_RUNETERRA_URL):
        self.lor_gg_url = lor_gg_url
        self.mastering_runeterra_url = mastering_runeterra_url
        self.all_cards = self._fetch_all_cards() 

    def _fetch_all_cards(self) -> dict:
        res = requests.get(self.lor_gg_url + 'storage/json/en_us/cardJson.json')
        res.raise_for_status()
        return res.json()

    def get_cards_from_code(self, code : str) -> list[str]:
        form_data = {
            'action': (None, 'liverfuncs_import_deck_code'),
            'code': (None, code)
        }
        res = requests.post(self.mastering_runeterra_url + 'wp-admin/admin-ajax.php', files=form_data)
        res.raise_for_status()
        return res.json()['cards']

    def get_cards_rarities(self) -> dict[str, Rarity]:
        rarities = {}
        for code, data in self.all_cards.items():
            rarity_name = data['rarityRef'].upper()
            try:
                rarity = Rarity[rarity_name]
                rarities[code] = rarity
            except:
                ...
        return rarities
    
    def get_cards_names(self) -> dict[str, str]:
        return {code : data['name'] for code, data in self.all_cards.items()}

    def _get_decks(self, format : str, page : int) -> list:
        res = requests.get(self.lor_gg_url + f'api/decks', params={
            'formatFilters[]': format,
            'page': page,
            'orderBy': 'matches',
            'orderByDirection': 'DESC'
        })
        res.raise_for_status()
        return res.json()

    def get_decks(self, matches_threshold : int = 100, format : Literal['Eternal', 'Standard'] = 'Eternal') -> pd.DataFrame:
        page = 1
        data = []
        while True:
            res_json = self._get_decks(format, page)
            if len(res_json) == 0:
                break
            data.extend(res_json)
            min_matches = min([int(item['matches']) for item in res_json])
            if min_matches<matches_threshold:
                break
            page += 1
        
        df = pd.DataFrame(data)
        for column in ['wins', 'matches']:
            df[column] = df[column].astype('int')
        df['winrate'] = df['winrate'].astype('float')

        return df[df['matches']>=matches_threshold]
    
parser = Parser()