#################################
##### Name: Karley Thurston
##### Uniqname: thurstkd
#################################

from bs4 import BeautifulSoup
import requests
import json
import secrets # file that contains your API key
SITE_CACHE = {}
n1= '\n'

class NationalSite():
    '''a national site

    Instance Attributes
    -------------------
    category: string
        the category of a national site (e.g. 'National Park', '')
        some sites have blank category.
    
    name: string
        the name of a national site (e.g. 'Isle Royale')

    address: string
        the city and state of a national site (e.g. 'Houghton, MI')

    zipcode: string
        the zip-code of a national site (e.g. '49931', '82190-0168')

    phone: string
        the phone of a national site (e.g. '(616) 319-7906', '307-344-7381')
    '''
    def __init__(self, category, name, address, zipcode, phone):
        self.category = category
        self.name = name
        self.address = address
        self.zipcode = zipcode
        self.phone = phone

    def info(self):
        return f'{self.name} ({self.category}): {self.address} {self.zipcode}'

def build_state_url_dict():
    ''' Make a dictionary that maps state name to state page url from "https://www.nps.gov"

    Parameters
    ----------
    None

    Returns
    -------
    dict
        key is a state name and value is the url
        e.g. {'michigan':'https://www.nps.gov/state/mi/index.htm', ...}
    '''
    
    BASE_URL = 'https://www.nps.gov'

    INDEX_PATH = '/index.htm'
    index_page_url = BASE_URL + INDEX_PATH

    response= requests.get(index_page_url)

    soup = BeautifulSoup(response.text, 'html.parser')

    state_parent = soup.find('ul', class_='dropdown-menu SearchBar-keywordSearch')
#   print(state_parent)
    state_lis = state_parent.find_all('li', recursive=False)
    state_sites = {}
    for state in state_lis:
        state_name = state_lis[state_lis.index(state)].text.strip().lower()
        state_tag = state.find('a')
        state_url = state_tag['href']
        state_sites[state_name] = BASE_URL + state_url
    return state_sites


def get_site_instance(site_url):
    '''Make an instances from a national site URL.
    
    Parameters
    ----------
    site_url: string
        The URL for a national site page in nps.gov
    
    Returns
    -------
    instance
        a national site instance
    '''
    #TODO: MAKE SURE NONE OPTIONS ARE ACCOUNTED FOR
    #BASE_URL = 'https://www.nps.gov'
    #index_page_url = BASE_URL + site_url
    response= requests.get(site_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    header_parent = soup.find('div', class_='Hero-titleContainer clearfix')
    #print(header_parent)

    name_block = header_parent.find('a')
    site_name = name_block.text

    category_block = header_parent.find('span', class_='Hero-designation')
    site_category = category_block.text.strip()

    footer_parent = soup.find('div', class_='vcard')

    #address:
    address_block = footer_parent.find('p')
    address_pieces = address_block.find_all('span')
    address_bits = []
    for piece in address_pieces:
        bit = piece.find_all('span')
        for b in bit:
            #print(b.text)
            address_bits.append(b.text)
    #print(address_bits)
    site_address = address_bits[0] + ", " + address_bits[1]
    site_zip = address_bits[2][0:5]

    #phone
    phone_block = footer_parent.find('span', class_='tel')
    site_phone = phone_block.text

    return NationalSite(site_category, site_name, site_address, site_zip, site_phone)

def get_sites_for_state(state_url):
    '''Make a list of national site instances from a state URL.
    
    Parameters
    ----------
    state_url: string
        The URL for a state page in nps.gov
    
    Returns
    -------
    list
        a list of national site instances
    '''
    response = requests.get(state_url)
    state_soup = BeautifulSoup(response.text, 'html.parser')

    site_parent = state_soup.find('ul', id='list_parks')
    site_lis = site_parent.find_all('li', recursive=False)
    #print(site_lis[0])
    BASE_URL = 'https://www.nps.gov'
    INDEX_PATH = 'index.htm'
    state_site_urls = []
    for site in site_lis:
        site_tag = site.find('a')
        site_url = site_tag['href']
        state_site_urls.append(BASE_URL+ site_url + INDEX_PATH)

    state_national_sites = []
    for url in state_site_urls:
        spot = state_site_urls.index(url) + 1
        park = get_site_instance(url)
        #print('[',spot,']',park.info())
        state_national_sites.append([spot, park.info(), park])
    return state_national_sites


def get_nearby_places(site_object):
    '''Obtain API data from MapQuest API.
    
    Parameters
    ----------
    site_object: object
        an instance of a national site
    
    Returns
    -------
    dict
        a converted API return from MapQuest API
    http://www.mapquestapi.com/search/v2/radius?key=KEY&maxMatches=4&origin=39.750307,-104.999472


MapQuest Radius Search /search/v2/radius
Origin
Radius
POI Category (i.e. SIC Code)
Max Matches
Ambiguities
Output Format

    '''

    #mapquest_base_url = 'http://www.mapquestapi.com/search/v2/radius'
    query_address = site_object.address.replace(" ", "+")

    if site_object.name in SITE_CACHE.keys():
        print("Using Cache")
        return SITE_CACHE[site_object.name]
    else:
        response = requests.get(f'http://www.mapquestapi.com/search/v2/radius?origin={query_address}+{site_object.zipcode}&radius=10&maxMatches=10&ambiguities=ignore&outFormat=json&key={secrets.consumer_key}')
        json_str = response.text
        query_result = json.loads(json_str)
    
        nearby_places = query_result['searchResults']
        places_list = []
        for place in nearby_places:
            print("Fetching")
            place_name = place['name']
            if place['fields']['group_sic_code_name_ext'] != '':
                place_category = place['fields']['group_sic_code_name_ext']
            else:
                place_category = 'no category'
            if place['fields']['address'] != '': 
                place_streetaddress = place['fields']['address']
            else:
                place_streetaddress = 'no address'
            if place['fields']['city'] != '':
                place_city = place['fields']['city']
            else:
                place_city = 'no city'
            places_list.append(f'-{place_name} ({place_category}): {place_streetaddress}, {place_city}')
            SITE_CACHE[site_object.name] = places_list
            #return f'-{place_name} ({place_category}): {place_streetaddress}, {place_city}{n1}'
        return places_list

state_nps_sites = build_state_url_dict()

while True:
    state_choice = input("1--Enter a US State to see all of its National Sites! To leave, type 'exit'. ")
    formatted_state_choice = state_choice.lower().strip()
    if type(state_choice) == str:
        if formatted_state_choice in state_nps_sites:
            destination_url = state_nps_sites[formatted_state_choice]
            #print(destination_url)
            national_site_list = get_sites_for_state(destination_url)
            print(f'----------------------------------------------{n1}  List of national sites in {formatted_state_choice}  {n1}----------------------------------------------')
            for site in national_site_list:
                print(f'[{site[0]}] {site[1]}')
            while True:
                site_choice = input("2--Choose a site number to see locations near the site. Type 'back' to see another state or 'exit' to leave. ")
                if site_choice == 'exit':
                    break
                elif site_choice == 'back':
                    break
                #elif site_choice.isnumeric() and 1<= int(site_choice) and int(site_choice) <=10:
                elif site_choice.isnumeric() and int(site_choice) <= (len(national_site_list) + 1) and int(site_choice) >=1:
                    numbered_site = national_site_list[int(site_choice)-1][2]
                    attractions = get_nearby_places(numbered_site)
                    print(f'----------------------------------------------{n1}  Places near {numbered_site.name}  {n1}----------------------------------------------')
                    for place in attractions:
                        print(place)
                    break
                else:
                    print("4--Please enter a valid site number.")
                    continue
            














###DO NOT TOUCH ME I WORK        
        elif formatted_state_choice =='exit':
            break
        else:
            print("6--Please enter a valid US state name or 'exit' to leave. ")
    elif type(state_choice) != str:
        print("7--Please enter a valid US state name or 'exit' to leave. ")
        break

if __name__ == "__main__":
    pass