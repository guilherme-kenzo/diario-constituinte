# Crawler and Text Extractions for the "diarios" of the Brazilian Constituent assembly (1987-1988)

This project was set up to run on a nix [devenv](https://devenv.sh/) and poetry. I believe, however, that using Poetry alone should suffice but this setup was not tested.

## Requirements

You should have at least [mupdf](https://mupdf.com/) and [poetry](https://python-poetry.org/) installed.

## How to crawl the data

To execute the crawler, run the following commands:

```bash
mkdir pdfs # Creates pdf folder
poetry install # installs python dependencies
python crawler.py 1987-01-01 1987-12-31 # crawl first year
python crawler.py 1988-01-01 1988-12-31 # crawl second year
 
```

The PDFs of the "diarios" will be downloaded to the pdfs folder.

## How to extract text from PDFs

```bash
mkdir extractions
python extract.py # this will iterate over files in /pdfs and extract them into /extractions
```

The dates can be adjusted to reflect your particular needs. The maximum range is 1 year because of the crawled sites limitations. 

The extracted text files will be available at the "extractions" folder.

## License

This project is licensed under the MIT license. 