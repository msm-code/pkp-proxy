from requests import Session
from pyquery import PyQuery as pq


class Ticket:
    def __init__(self, ticket_id, start, end, trains, starttime, endtime):
        self.ticket_id = ticket_id
        self.start = start
        self.end = end
        self.trains = trains
        self.starttime = starttime
        self.endtime = endtime

    @property
    def eventid(self):
        return f"TRAIN_{self.ticket_id}".encode().hex()



def get_raw_tickets_html(username, password):
    UA = "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0"
    session = Session()
    session.get("https://bilet.intercity.pl/", headers={"User-Agent": UA})
    r = session.post("https://bilet.intercity.pl/logowanie.jsp", data={
        "ref": "30",
        "login": username,
        "password": password,
        "actlogin": "Zaloguj+si%EA",
    }, headers={
        "User-Agent": UA,
        "Header": "https://bilet.intercity.pl",
        "Referer": "https://bilet.intercity.pl/logowanie.jsp",
    })
    return r.text


def parse_tickets(html):
    doc = pq(html)
    result = []
    for elm in doc(".black.table_div_row"):
        e = pq(elm)
        ticket_id = e(".first.table_div_cell a").text()
        relation = e(".table_div_cell_relacja").text()
        start, end, *trains = relation.split("\n")
        times = e(".table_div_cell_wyjazd_od_do").text().split("\n")
        starttime = f"{times[1]}T{times[5]}:00"
        endtime = f"{times[10]}T{times[14]}:00"
        result.append(Ticket(ticket_id, start, end, trains, starttime, endtime))
    return result
