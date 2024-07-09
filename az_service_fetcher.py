import sys
import os
import requests
import logging
import json
import ipaddress
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename="az_tags_retrieval.log")
# Attempt to assemble the link based on the date, this method is good unless holiday's introduce differences in the pattern
# or if the base URL changes for some reason
# An alternative would be to scrape the webpage for the URL, but that also relies on Microsoft not changing the layout of the page
today = datetime.today()
curr_mon = today - timedelta(days=today.weekday())
# Try to pull the JSON dated with the latest Monday
try:
    calculated_filename = f"ServiceTags_Public_{curr_mon.strftime('%Y%m%d')}.json"
    r = requests.get(f'https://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13A5DE5B63/{calculated_filename}', allow_redirects=True)
    r.raise_for_status()  # raises exception when not a 2xx response
    if r.status_code != 204:
        with open('service_tags.json', 'w') as output:
            output.write(json.dumps(r.json(), indent=4))
except Exception as e:
    logging.warning(f'- (LINE 21) {e}')
    # Try to pull the JSON dated with last week's Monday
    try:
        prev_mon = curr_mon - timedelta(days=curr_mon.weekday(), weeks=1)
        calculated_filename = f"ServiceTags_Public_{prev_mon.strftime('%Y%m%d')}.json"
        r = requests.get(f'https://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13A5DE5B63/{calculated_filename}', allow_redirects=True)
        r.raise_for_status()  # raises exception when not a 2xx response
        if r.status_code != 204:
            with open('service_tags.json', 'w') as output:
                output.write(json.dumps(r.json(), indent=2))
    except Exception as e2:
        logging.warning(f'- (LINE 32) {e2}')
        logging.info("- Failed to retreive most recent Public Service Tag Information")
        exit(1)
    logging.info("- Failed to retreive this week's Public Service Tag Information (New list not published or URL generated incorrectly) Using previous week's data...")

argument = sys.argv[1]
try:
    # See if we were given an IP address
    ip_addr = ipaddress.ip_address(argument)
except:
    try:
        # Otherwise, hopefully we got CIDR notation
        ip_addr = ipaddress.ip_network(argument)
    except:
        print("Please provide a valid IP address or CIDR as the only argument")
        exit(1)

try:
    service_tags = json.load(open('service_tags.json'))
except:
    print(f'Failed to open service_tags.json')
    exit(1)

# Because the address can be found in multiple places in the JSON, currently this will spit out multiple things saying similar things
# Some of these will mention the region, which IS useful to know (Would be nice to only get the 1 verbose response)
# match = None
for st in service_tags["values"]:
    # if not match:
        for cidr in st["properties"]["addressPrefixes"]:
            if str(ip_addr) == cidr or ip_addr in ipaddress.ip_network(cidr):
                match = {"name": st["name"], "cidr": cidr}
                print(f'CIDR Found for {argument}:\n {match["name"]} - {match["cidr"]}')
try:
    os.remove('service_tags.json')
except:
    print(f'Failed to delete service_tags.json')
    exit(1)