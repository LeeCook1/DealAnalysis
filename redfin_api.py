import re
import sys
import lxml
import pprint
import requests
import argparse
import dicttoxml

from redfin import Redfin
from bs4 import BeautifulSoup

from get_address import get_address


def below_the_fold(self, property_id, **kwargs):
    return self.meta_property('belowTheFold', {'propertyId': property_id, **kwargs}, page=True)


def get_property_data(address, client):
    property_id, listing_id = _get_property_ids(address, client)
    if not listing_id:
        print("Missing Listing ID")
    return client.below_the_fold(property_id)


def _get_property_ids(address, client):
    url = _get_redfin_url(address, client)
    initial_info = client.initial_info(url)
    property_id = initial_info['payload']['propertyId']
    listing_id = initial_info['payload'].get('listingId')
    return property_id, listing_id


def _get_redfin_url(address, client):
    response = client.search(address)
    return response['payload']['sections'][0]['rows'][0]['url']


def parse_data(data):
    parsed_data = {}
    data_xml = dicttoxml.dicttoxml(data)
    soup = BeautifulSoup(data_xml, 'lxml')
    keys = [
        'street', 'city', 'state', 'zip', 'countyName',
        'countyUrl', 'bed', 'bath', 'listingAgentName',
        'listingAgentNumber', 'listingBrokerName',
        'propertyTypeName', 'yearBuilt', 'lotSqft',
        'numStories', 'apn', 'taxableImprovementValue',
        'taxesDue', 'price', 'streetViewUrl']

    parsed_data = {key: soup.find(re.compile(key.lower())) for key in keys}
    parsed_data = {k: v.string for k, v in parsed_data.items() if v != None}
    return parsed_data


def init_args():
    args = get_args()
    args.address = get_address(args.address).address
    return args


def get_args():
    description = ''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('address', help='Property Address')
    return parser.parse_args()


def main():
    global args
    args = init_args()
    client = Redfin()
    data_json = get_property_data(args.address, client)
    parsed_data = parse_data(data_json)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(parsed_data)


Redfin.below_the_fold = below_the_fold

if __name__ == '__main__':
    main()
