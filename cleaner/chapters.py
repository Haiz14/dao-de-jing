from __future__ import annotations
from re import sub
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from bs4 import Tag, BeautifulSoup


class Chapter(TypedDict):
    title: str
    translation: str
    notes: str
    reference: str


class ChaptersParser:
    def __init__(self, source_soup: BeautifulSoup) -> None:
        self.soup = source_soup
        self.tables = self._get_all_chapter_tables()

    def _get_all_chapter_tables(self) -> list[Tag]:
        """
        All tables are contsiners for chapter.
        Except the first one is container for "Key to Nitations".
        And the last two (82, 83). They are just sime recerence.
        """
        return self.soup.find_all("table")[1:82]

    def get_chapters(self) -> dict[int, Chapter]:
        chapters = {}
        seq = 0
        for table in self.tables:
            chapter = self._parse_chapter_table(table)
            chapters[1] = chapter
            print(chapter)
            seq += 1
            print(seq)
            # chapters[chapter["title"]] = chapter
        return chapters

    def _parse_chapter_table(self, table: Tag) -> Chapter:
        title = table.previous_element.text  # type: ignore
        table_rows = table.find_all("tr")

        all_table_data = self._get_all_table_data(table)


        orignal_chinese_text = self._get_orignal_chinese_text(all_table_data[0])
        print(orignal_chinese_text)
        # translation = self._get_chapter_translation(all_table_data[1])
        return {}

    def _get_all_table_data(self, table) -> list[Tag]:
        all_table_data = []

        for table_row in table.find_all("tr"):
            all_table_data.extend(table_row.find_all("td"))

        if len(all_table_data) != 4:
            raise ValueError("All tables should have 4 td tags")
        return all_table_data

    def _get_chapter_translation(self, second_table_data: Tag) -> str:
        """
        Contains a bunch of p tags. Join them via \n and return a str.
        It is always 2nd table of of chapter table
        """
        return "\n".join([p.text for p in second_table_data.find_all("p")])

    def _get_orignal_chinese_text(self, first_table_data: Tag) -> str:
        """
        Contains a bunch of p tags.
        Each p tag contains an escaped chinese character in span tag
        """
        orignal_content = ""

        for p_tag in first_table_data.find_all("p"):
            tag_content = ""
            for span_tag in p_tag.find_all("span"):
                tag_content += span_tag.text

            # remove the irregularities
            partially_cleaned_tag_content = (
                tag_content.replace("\n", ", ")
                .replace("•,  ", "•")
            )
            # reolace (•) at the beginning with "(•) "
            cleaned_tag_content = sub(r"^\(•\)", "(•) ", partially_cleaned_tag_content)


            orignal_content += cleaned_tag_content + "\n"


        # remove the last \n
        return orignal_content[:-1]

    def _get_chapters_reference(self, third_table_data: Tag) -> str:
        """
              Contsins a bunch of p tags.
              Example p tag:
                <p class=MsoNormal><span style='font-size:11.0pt'>&#9830;<u>Heaven</u> and <u>earth</u>
        are <u>not</u> <u>kind</u>* –</span></p><p class=MsoNormal><span style='font-size:11.0pt'>&#9830;<u>Heaven</u> and <u>earth</u>

        """
        # preserve markfown underlines.
        chapter_reference = ""
        for p_tag in third_table_data.find_all("p"):
            content = p_tag.find("span").unwrap()

    def _get_chapters_notes(self, third_table_data: Tag) -> str:
        pass
