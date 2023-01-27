from html.parser import HTMLParser
from pathlib import Path


class MyParser(HTMLParser):
    def __init__(self, *, convert_charrefs: bool = ...) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self._tables = []
        self._daterow = True
        self._rowdates = []
        self._rowevents = []
        self._current_tag = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:

        self._current_tag = tag if tag != "i" else self._current_tag

        return super().handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        if tag == "table":
            self._tables.append(zip(self._rowdates, self._rowevents))
            self._rowdates = []
            self._rowevents = []

        if tag == "tr":
            self._daterow = ~self._daterow

        if tag == "body":
            print(self._tables)

        return super().handle_endtag(tag)

    def handle_data(self, data: str) -> None:
        if self._current_tag == "td":
            if self._daterow:
                self._rowdates.append(data)
            else:
                self._rowevents.append(data)

        return super().handle_data(data)


with Path("Sidoti Roster.htm").open() as f:
    html = f.read()
    parser = MyParser()
    parser.feed(html)
