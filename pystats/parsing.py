import matching
from datetime import datetime
from pprint import pprint

_connection_statuses = {
    "X": "aborted",
    "+": "may_keep_alive",
    "-": "will_close"
}

_date_format = "%d/%b/%Y:%H:%M:%S %z"

def parse_clf(value):
    return None if value == "-" else int(value)

def parse_value(token, value):
    match(token):
        case "connection_status":
            return _connection_statuses[value]
        case "hextid":
            return int(value, 16)
        case "time":
            return datetime.strptime(value[1:-1], _date_format)
        case _:
            return None

def parse(log_elements):
    out = {}
    for token in log_elements:
        type = matching.token_types[token]
        if type == "clf":
            out[token] = parse_clf(log_elements[token])
        elif type == None:
            out[token] = parse_value(token, log_elements[token])
        else:
            out[token] = type(log_elements[token])
    return out
