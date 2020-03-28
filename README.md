# Data Scraper AO3

This repository contains two scripts which extract data from A03 (http://archiveofourown.org/):

  * `extract_metadata.py`: extracts metadata of works which result from a specific search term on A03
  * `download_work.py`: downloads selected works as HTML from A03.
  
## Usage

### Extract metadata
`python extract_metadata.py <search term>`

Example usage:

`python extract_metadata.py "Harry Potter"`

### Download work
`python download_work.py <path_to_input.csv>  <path_to_output_dir>`

This script requires two input parameters
  1. csv-file which holds work IDs. This csv file must have a column `id` which holds the work IDs (e.g. `work_123`).
  2. path to a directory where you want to store the downloaded works. If the path does not exist it will be created by the script automatically.


Example usage:

`python download_work.py work_to_download.csv ./works`

Example csv-file:
```
id
work_123
work_456
work_7890
```

## References
This work resulted from a work cooperation with [Christina Schuster](https://ucris.univie.ac.at/portal/en/persons/christina-schuster(e7b3d645-e52e-434f-ae9c-7575e5036c02).html) (Uni:docs fellow and PraeDoc at the English Department at the University of Vienna, Austria).
Christina Schuster uses these scripts for her PhD project (ongoing) and examines representations of gender, sex/uality and identities in fanfiction.

Further information on her project as well as a link to her thesis will be provided at a later date.



## License
This work is licensed under the MIT license. Please check out the details in the LICENSE.txt

