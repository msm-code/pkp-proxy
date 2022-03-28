from intercity import get_raw_tickets_html, parse_tickets

from gcalendar import make_service_serviceaccount, add_train, train_added
import json

with open("config.json") as configf:
    config = json.load(configf)

ic = get_raw_tickets_html(config["username"], config["password"])
tickets = parse_tickets(ic)

service = make_service_serviceaccount()
for ticket in tickets:
    try:
        if train_added(service, ticket):
            break
        add_train(service, ticket)
    except Exception as e:
        print(repr(e))
        exit()
