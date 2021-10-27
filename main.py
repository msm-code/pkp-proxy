from intercity import get_raw_tickets_html, parse_tickets

from gcalendar import make_service, add_train
import json

with open("config.json") as configf:
    config = json.load(configf)

ic = get_raw_tickets_html(config["username"], config["password"])

tickets = parse_tickets(ic)

service = make_service()
for ticket in tickets:
    try:
        add_train(service, ticket)
    except Exception as e:
        exit()
