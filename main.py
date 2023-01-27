from html.parser import HTMLParser
from pathlib import Path
from icalendar import Event, Calendar
from datetime import datetime
import pytz


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
    cal = Calendar()
    file = Path("Sidoti Roster")
    with file.with_suffix(".htm").open() as f:
        html = f.read()
        parser = MyParser()
        parser.feed(html)
        shifts = []
        for date, event in zip(parser.dates, parser.events):

            if "\xa0" in event:
                continue

            shift = Event()
            date = datetime.strptime(date, "%a %d %b").replace(
                year=datetime.now().year, tzinfo=pytz.timezone("Australia/Sydney")
            )

            if "eve " in event.lower():
                start = date.replace(hour=14)
                end = date.replace(hour=23, minute=59)
            else:
                start = date.replace(hour=8)
                end = date.replace(hour=18)

            shift.add("summary", event)
            shift.add("dtstart", start)
            shift.add("dtend", end)
            shifts.append(shift)

        cal["dtstart"] = shifts[0]["dtstart"].to_ical()
        cal["summary"] = f"{file.stem}"

        for shift in shifts:
            cal.add_component(shift)

    file.with_suffix(".ics").write_bytes(cal.to_ical())
