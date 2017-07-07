# -*- coding: utf-8 -*-
"""
EDGE Timeshift checker
"""
import argparse
from datetime import datetime, timedelta
from requests import Session
from termcolor import colored


def check_timeshift(public_url, edge_url, api_version, resource):
    delta = timedelta(days=1)
    testing_from = (datetime.now() + delta).strftime('%Y-%m-%d')
    source_url = '{}/api/{}/{}?descending=1&offset={}&limit=1000'.format(
        public_url, api_version, resource, testing_from)
    test_url = '{}/api/{}/{}/'.format(edge_url, api_version, resource)
    r = Session()
    lr = Session()
    try:
        response = r.get(source_url).json()
    except Exception as e:
        print 'InvalidResponse: {}'.format(e.message)
        raise SystemExit

    while response['data']:
        for item in response['data']:
            l_resp = lr.get(test_url + item['id']).json()
            if (l_resp.get('data', {}).get('dateModified') !=
                    item['dateModified']):
                print colored('API - {}, EDGE - {}, ID: {}'.format(
                    item['dateModified'],
                    l_resp.get('data', {}).get('dateModified'),
                    item['id']), 'red')
            else:
                print colored('Pass: {} - {}'.format(
                    item['id'], item['dateModified']), 'green')
        next_page = response['next_page']['path']
        response = r.get(public_url + next_page).json()


def main():
    """
    Main function
    """
    parser = argparse.ArgumentParser(
        description="----- EDGE Timeshift checker -----")
    parser.add_argument('public_server', type=str,
                        help="https://api.public.org")
    parser.add_argument('edge_server', type=str,
                        help='http://my_edge_domain_or_ip')
    parser.add_argument('api_version', type=str, help='2.3')
    parser.add_argument(
        'resource', type=str,
        help='Document type for ckecking like: tenders, plans etc.')
    args = parser.parse_args()
    check_timeshift(args.public_server, args.edge_server, args.api_version,
                    args.resource)


#######################################################################
if __name__ == "__main__":
    main()
