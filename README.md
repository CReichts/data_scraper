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
TODO 



## License
This work is licensed under the MIT license. Please check out the details in the LICENSE.txt

