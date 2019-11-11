<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">
<img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>
<br />
This work and all the resulting documents (CSV, and others) are licensed under a 
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.

# lyrics_scraper
This project is the result of PRAC1 of the subject "Tipologia i cicle de vida de les dades" of the Master of Data 
Science of the UOC (Universitat Oberta de Catalunya).

## Description

This project has the capability to scrap the famous webpage https://www.azlyrics.com. To do so, the user can search
by artist, album, song or letter and generate an output file (csv) with the information of every song. 

This project is written in python3

## Installation

I recommend using a virtualenv in order not to install requirements in your system, thus creating possibles 
incompatibilities. 

### virtualenv

1. Create a virtualenv. Remember using python3  as interpreter.
    ```bash
    virtualenv -p python3 venv
    ```
2. Activate your new virtualenv
    ```bash
    source venv/bin/activate
    ```
3. Install the project requirements in your virtualenv.
    ```bash
    pip install -r requirements.txt
    ```

## Usage

It is intended to use it by calling the [main.py](main.py) file, that it contains some parameters to control several 
functionalities.

```bash
> python3 main.py -h

usage: main.py [-h] --output OUTPUT_FILE --search_by
               {artist,album,song,letter} --search SEARCH

Scrap azlyrics page

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT_FILE, -o OUTPUT_FILE
                        Output file name.
  --search_by {artist,album,song,letter}
                        Set how to search by parameter.
  --search SEARCH, -s SEARCH
                        Search the following string.
  --batch_size BATCH_SIZE
                        Set the request batch size.
```

### Example

```bash
python3 main.py --search_by 'artist' --search "pink floyd" -o output.csv
```

In this example, the _output.csv_ will contain the information and cleaned lyrics of all songs of the 'pink floyd'
artist.

## Output

Now, there's only one possible output format: csv.

The csv columns names are self-explanatory:
* artist
* album_name
* album_year
* album_category
* song_name
* song_genre
* song_lyrics

## Structure
```bash
.
├── main.py                 # Main file
├── README.md               # README.md
├── requirements.txt        # python requirements to be installed.
└── src
    ├── __init__.py
    ├── models.py           # Model output objects: Album, Artist, Song
    ├── outputer.py         # Functions to generate output files.
    ├── scraper
    │   ├── __init__.py
    │   ├── base.py         # Base abstract classes of the scraper.
    │   ├── exceptions.py   # Collection of custom exception classes.
    │   ├── plain.py        # Plain webpage scrapers.
    │   ├── requester.py    # Requester to perform batch requests.
    │   └── search.py       # Search webpage scrapers.
    ├── searcher.py         # Collection of search functions.
    └── utils.py            # Shared util functions.
```