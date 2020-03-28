#!/usr/bin/env python
"""Extracts metadata of works which result from a specific search term on archiveofourown.org.

The file requires the search term as input.

The following metadata are extracted: page, id, last_update, detailed_warnings, fandom, title,
text_link, archived_by, authors, gifted_to, characters, relationships, additional_tags, summary,
language, words, chapters, comments, kudos, bookmarks, hits, required_tags.

The extracted metadata are stored in csv format in the directory of execution (filename: documents_{search_query}.csv).

Example usage: python extract_metadata.py "Harry Potter"

Author: Magdalena Radinger
"""

import math
import numpy as np
import pandas as pd

import re
import requests
import sys
import time
import urllib.parse

from bs4 import BeautifulSoup

BASE_URL = 'https://archiveofourown.org'

RE_ARCHIVED_BY = re.compile('\[archived by .*\]$')
RE_AUTHOR_ARCHIVED_BY = re.compile('by .* \[archived by .*\]$')


def make_request(search_query, page=1, verbose=0):
    """
    Executes a HTTP-GET request for the given search query and page.

    Parameters
    ----------
    search_query the string to search for
    page number of the result page

    Returns
    -------
    the content of the response as BeautifulSoup
    """

    rlink = BASE_URL + '/works/search?utf8=%E2%9C%93&work_search%5Bquery%5D=' + \
            urllib.parse.quote_plus(search_query) + \
            '&work_search%5Btitle%5D=&work_search%5Bcreators%5D=&work_search%5Brevised_at%5D=&' + \
            'work_search%5Bcomplete%5D=&work_search%5Bcrossover%5D=&work_search%5Bsingle_chapter%5D=0&' + \
            'work_search%5Bword_count%5D=&work_search%5Blanguage_id%5D=&work_search%5Bfandom_names%5D=&' + \
            'work_search%5Brating_ids%5D=&work_search%5Bcharacter_names%5D=&work_search%5Brelationship_names%5D=&' + \
            'work_search%5Bfreeform_names%5D=&work_search%5Bhits%5D=&work_search%5Bkudos_count%5D=&' + \
            'work_search%5Bcomments_count%5D=&work_search%5Bbookmarks_count%5D=&' + \
            'work_search%5Bsort_column%5D=revised_at&work_search%5Bsort_direction%5D=asc&commit=Search'

    rlink = rlink + '&page={:d}'.format(page)

    if verbose > 0:
        print('Request link', rlink)

    r = requests.get(rlink)

    return BeautifulSoup(r.content, 'html.parser')


def convert_list_to_str(list_to_convert):
    """
    Converts the given list of str elements to a comma-separated str of the elements.
    This is used to make list-output in csv more readable.

    Parameters
    ----------
    list_to_convert list of str elements

    Returns
    -------
    A string which contains the elements of the list comma-separatedly.

    """
    return ', '.join(list_to_convert)


def get_results(search_query, page=1):
    """
    Gets the metadata per work result for the given search query and result page.

    Parameters
    ----------
    search_query the string to search for
    page number of the result page

    Returns
    -------
    A list of dictionaries which hold the metadata of the resulting works.
    """
    soup = make_request(search_query=search_query, page=page)

    processed_results = 0
    documents = []

    # go through results on this page and extract metadata
    for link in soup.findAll('li', {'class': 'work blurb group'}):
        document = dict()

        document['page'] = page
        document['id'] = link['id']

        for dolutag in link.findAll('p', {'class': 'datetime'}):
            document['last_update'] = dolutag.text

        for detailedwarntag in link.findAll('span', {'class': 'text'}):
            document['detailed_warnings'] = detailedwarntag.text

        for headtag in link.findAll('h5', {'class': 'fandoms heading'}):

            fandom_tags = []

            for fandomtag in headtag.findAll('a', {'class': 'tag'}, href=True, text=True):
                fandom_tags.append(fandomtag.text)

            document['fandom'] = convert_list_to_str(fandom_tags)

        for headtag in link.findAll('h4', {'class': 'heading'}):
            authors = []
            gifted_to = []

            # check if archived by
            headtag_txt = ' '.join(headtag.text.replace('\n', '').split())
            archived_by_txt = RE_ARCHIVED_BY.search(headtag_txt)
            archived_by_name = None
            if archived_by_txt:
                archived_by_name = archived_by_txt.group(0).replace('[archived by ', '').replace(']', '')
                author_extracted = RE_AUTHOR_ARCHIVED_BY.search(headtag_txt)

                if author_extracted:
                    authors_extr = author_extracted.group(0).split(' [')[0].replace('by ', '').split(',')
                    for author in authors_extr:
                        authors.append(author)

            for tag in headtag.findAll('a', href=True, text=True):
                if tag['href'].startswith('/works'):
                    document['title'] = tag.text
                    document['text_link'] = BASE_URL + tag['href']

                elif tag['href'].endswith('/gifts') or tag['href'].startswith('/gifts'):
                    gifted_to.append(tag.text)

                elif tag['rel'] == ['author'] and archived_by_name is None:
                    # when archived_by_name is set, then the authors were already extracted
                    authors.append(tag.text)

            document['archived_by'] = archived_by_name
            document['authors'] = convert_list_to_str(authors)
            document['gifted_to'] = convert_list_to_str(gifted_to)

        characters = []
        for charactertag in link.findAll('li', {'class': 'characters'}):
            characters.append(charactertag.text)

        document['characters'] = convert_list_to_str(characters)

        relationships = []
        for relationtag in link.findAll('li', {'class': 'relationships'}):
            relationships.append(relationtag.text)

        document['relationships'] = convert_list_to_str(relationships)

        add_tags = []
        for addtag in link.findAll('li', {'class': 'freeforms'}):
            add_tags.append(addtag.text)

        document['additional_tags'] = convert_list_to_str(add_tags)

        for summarytag in link.findAll('blockquote', {'class': 'userstuff summary'}):
            document['summary'] = summarytag.text.replace('\n', '')

        for statstag in link.findAll('dl', {'class': 'stats'}):
            for langtag in statstag.find_all("dd", class_="language"):
                document['language'] = langtag.text

            for wordtag in statstag.find_all("dd", class_="words"):
                document['words'] = wordtag.text.replace(',', '')

            for chaptertag in statstag.find_all("dd", class_="chapters"):
                document['chapters'] = ' ' + chaptertag.text  # add space so Excel does not interpret is as date

            for commentstag in statstag.find_all("dd", class_="comments"):
                for a_cmt in commentstag.find_all('a'):
                    document['comments'] = a_cmt.text

            for kudotag in statstag.find_all("dd", class_="kudos"):
                document['kudos'] = kudotag.text

            for bookmarktag in statstag.find_all("dd", class_="bookmarks"):
                document['bookmarks'] = bookmarktag.text

            for hittag in statstag.find_all("dd", class_="hits"):
                document['hits'] = hittag.text

        # required tags
        req_tags = link.find_all('ul', class_='required-tags')

        list_req_tags = []
        for req_tag in req_tags:
            req_tag_texts = req_tag.find_all('span', class_='text')
            for req_tag_text in req_tag_texts:
                list_req_tags.append(req_tag_text.text)

        document['required_tags'] = convert_list_to_str(list_req_tags)

        documents.append(document)
        processed_results += 1

    return processed_results, documents


if __name__ == "__main__":
    search_term = str(sys.argv[1])

    start_time = time.time()
    total_processed_results = 0

    # make first request with search to extract number of total results
    soup = make_request(search_query=search_term, verbose=1)
    total_results = int(soup.find_all('h3', class_='heading')[1].text.split(' ')[0])
    max_page = math.ceil(total_results / 20)
    time.sleep(5)

    page = 1
    total_documents = []

    while total_processed_results < total_results and page <= max_page:
        print(f'page {page}/{max_page}')
        processed_results, documents = get_results(search_term, page)

        total_processed_results += processed_results
        total_documents.extend(documents)

        page += 1
        if total_processed_results < total_results:
            time.sleep(5)

    pd.DataFrame(total_documents).to_csv('documents_{search_query}.csv'.format(
        search_query=search_term),
        index=False,
        sep=';')

    end_time = time.time()
    print(f'Execution time {np.round(end_time - start_time, 1)}sec')
