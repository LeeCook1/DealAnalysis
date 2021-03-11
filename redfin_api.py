import re
import lxml
import dicttoxml

from redfin import Redfin
from bs4 import BeautifulSoup

def get_property_data(address):
    property_id,listing_id = _get_property_ids(address)
    return client.below_the_fold(property_id, listing_id)

def _get_property_ids(address):
    url = _get_redfin_url(address)
    initial_info = client.initial_info(url)
    property_id = initial_info['payload']['propertyId']
    listing_id = initial_info['payload'].get('listingId')
    return property_id, listing_id

def _get_redfin_url(addres):
    response = client.search(address)
    return response['payload']['sections'][0]['rows'][0]['url']

def parse_data(data):
    parsed_data = {}
    data_xml = dicttoxml.dicttoxml(data)
    soup = BeautifulSoup(data_xml,'lxml')
    keys = [
            'street', 'city', 'state', 'zip',
            'countyName', 'listingAgentName',
            'listingAgentNumber', 'listingBrokerName',
            'bed', 'bath', 'propertyTypeName', 
            'yearBuilt', 'lotSqft', 'numStories', 
            'apn', 'taxableImprovementValue',
            'taxesDue', 'price','streetViewUrl']
    
    parsed_data = { key: soup.find(re.compile(key.lower())) for key in keys } 
    parsed_data = { k: v.string for k, v in parsed_data.items() if v }
    return parsed_data

def main():
    global client
    client = Redfin()
    address = '4544 Radnor St, Detroit Michigan'
    data_json = get_property_data(address)
    parsed_data = parse_data(data_json)
#'2263 Sewell Mill Rd, Marietta, GA'
client = Redfin()
