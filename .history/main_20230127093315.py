from html.parser import HTMLParser
from pathlib import Path
from icalendar import cal


class MyParser(HTMLParser):
    def __init__(self, *, convert_charrefs: bool = ...) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self._daterow = True
        self._rowdates = []
        self._rowevents = []
        self._current_tag = ""
        self.dates = []
        self.events = []

    def handle_starttag(self, tag: str, attrs) -> None:

        self._current_tag = tag if tag != "i" else self._current_tag

        if tag == "hr":
            self.dates = self._rowdates.copy()
            self.events = self._rowevents.copy()

        return super().handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:

        if tag == "tr":
            self._daterow = not self._daterow

        if tag == "body":
            print("Dates:", self.dates, "\n")
            print("Events:", self.events)

        self._current_tag = ""
        return super().handle_endtag(tag)

    def handle_data(self, data: str) -> None:
        if self._current_tag == "td":
            if self._daterow:
                self._rowdates.append(data)

            else:
                self._rowevents.append(data)

        return super().handle_data(data)


if __name__ == "__main__":
    with Path("Sidoti Roster.htm").open() as f:
        html = f.read()
        parser = MyParser()
        parser.feed(html)
