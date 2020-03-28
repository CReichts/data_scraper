#!/usr/bin/env python
"""Downloads selected works from archiveofourown.org.

The script requires two inputs: csv-file and output_directory.

Through the csv_file the work IDs which should be downloaded are provided. It  must hold a column 'id'
which holds the work-IDs (e.g. work_100).

The files are downloaded to the output_directory, existing files with the same name are overwritten. If the path
does not exist, it will be created automatically.

Example usage: python download_work.py input.csv ./path/to/output

Author: Magdalena Radinger
"""

import numpy as np
import os
import pandas as pd
import requests
import sys
import time

from bs4 import BeautifulSoup

BASE_URL = 'https://archiveofourown.org'


def download(work_id, directory='.'):
    """Download given work as html into the given directory.

    Parameters
    ----------
    work_id id of work to download
    directory directory in which the downloaded work should be saved (default current directory)

    Returns True if download successful, False otherwise.
    -------

    """
    r = requests.get(BASE_URL + '/works/' + work_id)
    work_page = BeautifulSoup(r.content, 'html.parser')

    for downloads in work_page.find_all('li', {'class': 'download'}):
        for html_download in downloads.find_all('a', text="HTML"):
            time.sleep(5)  # delay required to not be blocked by website (bot detection)
            html_page = BeautifulSoup(requests.get(BASE_URL + html_download['href']).content, 'html.parser')
            file_path = '{:s}/{:s}.html'.format(directory, work_id)

            with open(file_path, 'w', encoding='utf-8') as f_out:
                f_out.write(html_page.prettify())
                return True

    return False


if __name__ == "__main__":
    csv_input = str(sys.argv[1])
    output_directory = str(sys.argv[2])

    start_time = time.time()
    df_works = pd.read_csv(csv_input)

    # create output directory if not exists
    os.makedirs(output_directory, exist_ok=True)

    for work_id in df_works['id'].str.replace('work_', ''):
        if not download(work_id=work_id, directory=output_directory):
            print(f'Work {work_id} could not be downloaded')

        time.sleep(5)  # delay required to not be blocked by website (bot detection)

    end_time = time.time()
    print(f'Execution time {np.round(end_time - start_time, 0)}sec ')
