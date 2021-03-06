from __future__ import print_function

import sys
import time
import datetime
import argparse

import requests

from astropy.table import Table, Column, vstack

from scrape import COURSE_DETAIL_URL

COURSE_DETAIL_URL = 'https://webproc.mnscu.edu/registration/search/detail.html?campusid=072&courseid={course_id}&yrtr={year_term}&rcid=0072&localrcid=0072&partnered=false&parent=search'


def class_exists_for_cid(cid, year_term):
    course_url = COURSE_DETAIL_URL.format(course_id=cid, year_term=year_term)
    result = requests.get(course_url)
    return 'System Error' not in result.text


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Discover CID numbers')
    parser.add_argument('--year-term',action='store',
                        help='Code for year/term, a 5 digit '
                        'number like 20155 (spring of 2015)')
    parser.add_argument('--max-cid', action='store', default=4000,
                        help='The largest course ID number to look for.')
    args = parser.parse_args()

    year_term = args.year_term
    max_cid = args.max_cid

    overall_table = None

    # Generate a date/time to use in naming directory with results
    now = time.localtime()
    formatted_datetime = datetime.datetime(*now[:-3]).isoformat()
    formatted_datetime = formatted_datetime.replace(':', '-')

    good_cids = []
    for cid in range(1, int(max_cid) + 1):
        cid_str = '{:06d}'.format(cid)
        print('Checking {}\r'.format(cid_str), end='')
        sys.stdout.flush()
        if class_exists_for_cid(cid_str, year_term):
            good_cids.append(cid_str)
    print('Total of {} good CIDs found'.format(len(good_cids)))
    if good_cids:
        results = Table(data=[good_cids, [year_term] * len(good_cids)],
                        names=['ID #', 'year_term'])
        results.write('{}-good-cids.csv'.format(year_term))
