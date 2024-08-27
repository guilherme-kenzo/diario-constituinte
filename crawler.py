from requests_html import HTMLSession
from requests import exceptions
from time import sleep
from glob import glob
from datetime import datetime
import os
import re
import click


SESSION = HTMLSession()

def _get_w_retry(url, attempts=1, max_attempts=10):
    if attempts >= max_attempts:
        return None
    try:
        print(url)
        r = SESSION.get(url)
    except exceptions.ConnectionError as e:
        print(e)
        r = _get_w_retry(url, attempts=attempts+1)
    return r

def _check_if_doc_already_exists(file_name):
    existing_files = [i.split('/')[-1] for i in glob("pdfs/*pdf")]
    return file_name in existing_files


def get_init_page(initial_date: datetime, final_date: datetime):
    return SESSION.get(("https://imagem.camara.gov.br/prepara.asp?selDataIni="
                        f"{initial_date.strftime('%d/%m/%Y')}"
                        f"&selDataFim={final_date.strftime('%d/%m/%Y')}"
                        "&opcao=1&selCodColecaoCsv=R"))

def get_relevant_links(init_page):
    days = init_page.html.find('td.calWeekDaySel')
    urls = []
    for i in days:
        url = i.find('a', first=True).absolute_links.pop()
        urls.append(url)
    return urls

def get_page_content(url):
    r = SESSION.get(url)
    try:
        pdf_url = re.search(r'http://.+?pdf#page=', r.text, flags=re.I).group()
    except AttributeError as e:
        raise Exception("Got an error: {error}. Extraction of the url from the page failed." 
               " The page content is: " + r.text.format(error=e))
        
    print(f"Downloading pdf at {pdf_url}")
    r = _get_w_retry(pdf_url)
    file_name = pdf_url.split('/')[-1].strip('#page=')
    return r.content, file_name

def save_pdf_file(file_name, content):
    with open(os.path.join("pdfs", file_name), 'wb') as f:
        f.write(content)

@click.command()
@click.argument('initial_date', type=click.DateTime())
@click.argument('final_date', type=click.DateTime())
def main(initial_date, final_date):
    init_page = get_init_page(initial_date=initial_date, final_date=final_date)
    urls = get_relevant_links(init_page)
    for i in urls:
        content, file_name = get_page_content(i)
        if _check_if_doc_already_exists(file_name):
            print("File already exists.")
            continue
        save_pdf_file(file_name, content)


if __name__ == "__main__":
    main()