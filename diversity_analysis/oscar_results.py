import re
import sys
import collections
import contextlib
import csv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

OMDB_API = "6c0455f8"
FIELDS = ["year", "award", "won", "nominee", "nominated_film", "addl_notes", "special_citation"]
OscarNomination = collections.namedtuple("OscarNomination", FIELDS)

@contextlib.contextmanager
def get_driver():
    try:
        opts = Options()
        opts.headless = False
        driver = webdriver.Firefox(options=opts)
        driver.get("http://awardsdatabase.oscars.org/")
        yield driver
    finally: 
        driver.close()

@contextlib.contextmanager
def get_writer(filepath=None):
    """Yields a csv DictWriter object.

    Parameters
    ----------
    filepath: Option[str]
        The path to a file. If filepath is None, the file goes to stdout.
    """
    try:
        csvfile = sys.stdout if filepath is None else open(filepath, "w")
        yield csvfile
    finally:
        if filepath is not None:
            csvfile.close()

def conduct_search(driver, award_category="Best Picture"):
    if isinstance(award_category, str):
        award_category = [award_category]
    award_category = set(award_category)
    elem = driver.find_element_by_css_selector(
        "button.awards-basicsrch-awardcategory"
        )
    elem.click()
    dropdown = driver.find_element_by_css_selector(
        "ul.multiselect-container"
    )
    award_categories = dropdown.find_elements_by_tag_name("li")
    select_categories = [
        item for item in award_categories
        if " ".join(item.text.split()).strip() in award_category
    ]
    for category in select_categories:
        category.find_element_by_tag_name("a").send_keys(Keys.RETURN)
    search = driver.find_element_by_id("btnbasicsearch")
    search.click()

def get_html(driver):
    return BeautifulSoup(driver.page_source, "html.parser")

def _clean_text(elem: BeautifulSoup) -> str:
    """Strips whitespace and converts the text of a BeautifulSoup object into titlecase"""
    elem_text = elem.text if elem is not None else ""
    return " ".join(elem_text.split()).strip()

def get_results(html):
    results_container = html.find(id="resultscontainer")
    results = results_container.find_all("div", class_="awards-result-chron")
    for year_result in results:
        year_div = year_result.find("div", class_="result-group-title")
        year = re.sub(r"\s*\([0-9]+(?:st|nd|rd|th)\s*\)", "", year_div.text).strip()
        for award in year_result.find_all("div", class_="result-subgroup"):
            award_name = _clean_text(award.find("div", class_="result-subgroup-title"))
            result_items = award.find("div", class_="awards-result-subgroup-items")
            for nomination in result_items.find_all("div", class_="result-details"):
                won = nomination.find("span", title="Winner") is not None
                nominee = _clean_text(
                    nomination.find("div", class_="awards-result-nominationstatement")
                )
                notes_text = _clean_text(
                    nomination.find("div", class_="awards-result-publicnote")
                )
                addl_notes = re.sub(r"\[\s*NOTE:\s*(.*)\s*\]", r"\1",notes_text)
                special_citation = _clean_text(
                    nomination.find("div", class_="awards-result-descandcitation")
                )
                film_nominated = _clean_text(
                    nomination.find("div", class_="awards-result-film")
                )
                nomination_record = OscarNomination(
                    year,
                    award_name,
                    won,
                    nominee,
                    film_nominated,
                    addl_notes,
                    special_citation
                )
                yield nomination_record._asdict()

def write_results(dict_results, filepath):
    with get_writer(filepath) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDS)
        writer.writeheader()
        for result in dict_results:
            writer.writerow(result)

def scrape_oscars(category, filepath):
    with get_driver() as driver:
        conduct_search(driver, category)
        results = get_results(get_html(driver))
    write_results(results, filepath)

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Scrapes data from the Oscar nominations database"
    )
    parser.add_argument(
        "category",
        nargs="+",
        help="The names of categories you want to scrape"
    )
    parser.add_argument(
        "--output",
        "-o",
        help="The file to save your results to. Prints to stdout if not specified"
    )
    args = parser.parse_args()
    scrape_oscars(args.category, args.output)

if __name__ == "__main__":
    main()