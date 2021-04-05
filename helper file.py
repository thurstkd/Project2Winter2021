from bs4 import BeautifulSoup
import requests
import json
import secrets
"""
First, your program will ask a user to input a state name (case-insensitive).
Second, to pass the included tests, you will need to edit the function in the starter
code get_sites_for_state(state_url) that takes a state page URL (e.g.
“https://www.nps.gov/state/az/index.htm”) and returns a list of NationalSite
objects in the state page.
Third, based on the returned value from get_sites_for_state(state_url), print
national sites in the state in the following format: [number] <name> (<type>):
<address> <zip code>.
Example : [1] Isle Royale (National Park): Houghton, MI 49931
"""

class NationalSite:
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
#TODO there are stupid spaces here
    def info(self):
        print(self.name," (",self.category,"): ",self.address," ",self.zipcode)
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
    #print(state_lis[0].text.strip())
    state_sites = {}
    for state in state_lis:
        state_name = state_lis[state_lis.index(state)].text.strip().lower()
        state_tag = state.find('a')
        state_url = state_tag['href']
    #    print(state_name)
    #    print(state_url)
        state_sites[state_name] = BASE_URL + state_url
    #print(state_sites['washington'])
    return state_sites


state_nps_sites = build_state_url_dict()
#print(state_nps_sites)
#print(state_nps_sites['michigan'])
#print state_nps_sites.keys()

"""
while True:
    state_choice = input("Enter a US State to see all of its National Sites! ")
    formatted_state_choice = state_choice.lower().strip()
    if type(state_choice) == str:
        if formatted_state_choice in state_nps_sites:
            destination_url = state_nps_sites[formatted_state_choice]
            #print(destination_url)
            break
        elif formatted_state_choice not in state_nps_sites:
                    print("Please enter a valid US state name. ")
    elif type(state_choice) != str:
        print("Please enter a valid US state name. ")
        break
"""


response2 = requests.get('https://www.nps.gov/state/ca/index.htm')

state_soup = BeautifulSoup(response2.text, 'html.parser')

site_parent = state_soup.find('ul', id='list_parks')
#print(site_parent)
site_lis = site_parent.find_all('li', recursive=False)
#print(site_lis[0])
BASE_URL = 'https://www.nps.gov'
INDEX_PATH = 'index.htm'
state_site_urls = []
for site in site_lis:
    site_tag = site.find('a')
    site_url = site_tag['href']
    #    print(state_name)
    #print(site_url)
    state_site_urls.append(BASE_URL+ site_url + INDEX_PATH)
    #print(state_sites['washington'])
#print(state_site_urls)
#return state_sites
##H3HREF and use exiting 



"""

<div class="col-md-9 col-sm-9 col-xs-12 table-cell list_left">
<h2>National Historical Reserve</h2>
<h3><a href="/ebla/" id="anch_12">Ebey's Landing</a></h3>
<h4>Coupeville, WA</h4>
<p>
This stunning landscape at the gateway to Puget Sound, with its rich farmland and promising seaport, lured the earliest American pioneers north of the Columbia River to Ebey’s Landing. Today Ebey’s Landing National Historical Reserve preserves the historical, agricultural and cultural traditions of both Native and Euro-American – while offering spectacular opportunities for recreation.
</p>
</div>
<div class="col-md-3 col-sm-3 col-xs-12 result-details-container table-cell list_right">
<div class="col-md-12 col-sm-12 col-xs-6 noPadding stateThumbnail">
<img class="stateResultImage" src="/customcf/apps/CMS_HandF/ParkSearchPics/B81D7430-1DD8-B71C-0ED7826B4048F91F.jpg" alt="Ferry House from across the Prairie" border="0">
</div>
<div class="col-md-12 col-sm-12  noPadding stateListLinks">
<ul>
<li><a href="http://www.nps.gov/ebla/planyourvisit/conditions.htm" id="anch_13"> Alerts &amp; Conditions<span class="hidden-xs"> »</span></a></li>
<li><a href="http://www.nps.gov/ebla/planyourvisit/basicinfo.htm" id="anch_14"> Basic Information<span class="hidden-xs"> »</span></a></li>
<li><a href="http://www.nps.gov/ebla/planyourvisit/calendar.htm" id="anch_15"> Calendar<span class="hidden-xs"> »</span></a></li>
<li><a href="http://www.nps.gov/ebla/planyourvisit/maps.htm" id="anch_16"> Maps<span class="hidden-xs"> »</span></a></li>
</ul>
</div>
</div>
"""
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
    if category_block.text.strip() != '':
        site_category = category_block.text.strip()
    else:
        site_category = "Other"

    footer_parent = soup.find('div', class_='vcard')
    print(footer_parent)
    #address:
    address_block = footer_parent.find('p')
    address_pieces = address_block.find_all('span')
    print(address_pieces)
    address_bits = []
    for piece in address_pieces:
        bit = piece.find_all('span')
        for b in bit:
            print(b.text)
            address_bits.append(b.text)
    print(len(address_bits))
    site_address = address_bits[0] + ", " + address_bits[1]
    site_zip = address_bits[2][0:5]

    #phone
    phone_block = footer_parent.find('span', class_='tel')
    site_phone = phone_block.text
    print(site_phone)

    return NationalSite(site_category, site_name, site_address, site_zip, site_phone)

Channel_Islands = get_site_instance('https://www.nps.gov/chis/index.htm')
print(Channel_Islands.info())
print(state_nps_sites['california'])
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

#cali_sites = get_sites_for_state('https://www.nps.gov/state/ca/index.htm')
#print(cali_sites)