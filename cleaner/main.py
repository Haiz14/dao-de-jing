from pathlib import Path
from bs4 import BeautifulSoup, Tag

from chapters import ChaptersParser

SRC_HTML_PATH = Path("../source.html")


def get_src_soup() -> BeautifulSoup:
    with open(SRC_HTML_PATH, mode="r") as html_file:
        src_html = html_file.read()
    return BeautifulSoup(src_html, "html.parser")


def get_all_chapters_title(soup: BeautifulSoup) -> list[Tag]:
    """
    Chspter titles are present just before
    the table tags.
    Except for the first table tag foumd.
    The first tag before its is "Ket to Notations"
    """
    tables: list[Tag] = soup.find_all("table")
    p_tags_before_table_elements: list[Tag] = []
    for table in tables:
        p_tags_before_table_elements.append(table.find_previous("p"))  # type: ignore
        print(table.attrs)
    return p_tags_before_table_elements[2:]


def main():
    src_soup = get_src_soup()
    parser = ChaptersParser(src_soup)
    parser.get_chapters()


if __name__ == "__main__":
    main()
