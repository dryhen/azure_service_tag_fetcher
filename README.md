# azure_service_tag_fetcher
This script aims to fetch the latest list of Azure public IP addresses and service tags for a given IP address/CIDR range.

## Why?
There are many scenarios where finding out what service an IP address belongs to is helpful. (E.g. When someone is working with firewalls.)
Given how IP addresses in the cloud can change relatively often, it can be difficult to keep track of which ones are associated with which services.
(Can be necessary to know if you aren't able to work with domain names.)

## Downsides to this script
This script tries to determine the download link for the latest public service tags JSON programatically. This means if Microsoft makes a change to the typical
download URL this script will be rendered non-functional.

## Usage

`python3 az_service_fetcher.py <IP address or CIDR>`

e.g. `python3 az_service_fetcher.py 4.232.99.0/24` or `python3 az_service_fetcher.py 4.232.99.1`