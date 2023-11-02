import re

# "%v:%p %h %l %u %t \"%r\" %s:%>s %I %O \"%{Referer}i\" \"%{User-Agent}i\" %D %k %f \"%U\" \"%q\""
# %v:%p %h %l %u %t "%r" %s:%>s %I %O "%{Referer}i" "%{User-Agent}i" %D %k %f "%U" "%q"
# ^(\S+):(\d+) (\S+) (\S+) (\S+) (\[.+\]) "(.*)" (\d+):(\d+) (\d+) (\d+) "(.*)" "(.*)" (\d+) (\d+) (\S+) "(.*)" "(.*)"$

# "%v:%p %h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\" %a %A %b %B %D %f %H %k %L %m %P \"%U\" \"%q\" %R %T %V %X %I %S"
# %v:%p %h %l %u %t "%r" %>s %O "%{Referer}i" "%{User-Agent}i" %a %A %b %B %D %f %H %k %L %m %P "%U" "%q" %R %T %V %X %I %S
# ^(\S+):(\d+) (\S+) (\S+) (\S+) (\[.+\]) \"(.*)\" (\d+) (\d+) \"(.*)\" \"(.*)\" (\S+) (\S+) (-|\d+) (\d+) (\d+) (\S+) (\S+) (\d+) (-|\d+) (\S+) (\d+) \"(.*)\" \"(.*)\" (\S+) (\d+) (\S+) (X|\+|-) (\d+) (\d+)$

tokens = {
    "%a": {
        "name": "client_ip",
        "regex": r"\S+"
    },
    "%{c}a": {
        "name": "underlying_peer_ip",
        "regex": r"\S+"
    },
    "%A": {
        "name": "local_ip",
        "regex": r"\S+"
    },
    "%B": {
        "name": "response_size",
        "regex": r"\d+"
    },
    "%b": {
        "name": "response_size_clf",
        "regex": r"-|\d+"
    },
    "%D": {
        "name": "time_to_serve_us",
        "regex": r"\d+"
    },
    "%f": {
        "name": "filename",
        "regex": r"\S+"
    },
    "%h": {
        "name": "remote_hostname",
        "regex": r"\S+"
    },
    "%{c}h": {
        "name": "underlying_remote_hostname",
        "regex": r"\S+"
    },
    "%H": {
        "name": "request_protocol",
        "regex": r"\S+"
    },
    "%k": {
        "name": "keepalive_count",
        "regex": r"\d+"
    },
    "%l": {
        "name": "remote_logname",
        "regex": r"\S+"
    },
    "%L": {
        "name": "error_log_id",
        "regex": r"-|\d+"
    },
    "%m": {
        "name": "request_method",
        "regex": r"\S+"
    },
    "%p": {
        "name": "port",
        "regex": r"\d+"
    },
    "%{canonical}p": {
        "name": "canonical_port",
        "regex": r"\d+"
    },
    "%{local}p": {
        "name": "local_port",
        "regex": r"\d+"
    },
    "%{remote}p": {
        "name": "remote_port",
        "regex": r"\d+"
    },
    "%P": {
        "name": "pid",
        "regex": r"\d+"
    },
    "%{pid}P": {
        "name": "pid_alt",
        "regex": r"\d+"
    },
    "%{tid}P": {
        "name": "tid",
        "regex": r"\d+"
    },
    "%{hextid}P": {
        "name": "hextid",
        "regex": r"(?:0[xX])?[0-9a-fA-F]+"
    },
    "%q": {
        "name": "query",
        "regex": r".*"
    },
    "%r": {
        "name": "first_line",
        "regex": r".*"
    },
    "%R": {
        "name": "handler",
        "regex": r"\S+"
    },
    "%s": {
        "name": "status",
        "regex": r"\d+"
    },
    "%>s": {
        "name": "final_status",
        "regex": r"\d+"
    },
    "%t": {
        "name": "time",
        "regex": r"\[.+\]"
    },
    "%T": {
        "name": "time_to_serve_s",
        "regex": r"\d+"
    },
    "%u": {
        "name": "remote_user",
        "regex": r"\S+"
    },
    "%U": {
        "name": "url",
        "regex": r".*"
    },
    "%v": {
        "name": "server_name",
        "regex": r"\S+"
    },
    "%V": {
        "name": "server_name_ucn",
        "regex": r"\S+"
    },
    "%X": {
        "name": "connection_status",
        "regex": r"X|\+|-"
    },
    "%I": {
        "name": "bytes_received",
        "regex": r"\d+"
    },
    "%O": {
        "name": "bytes_sent",
        "regex": r"\d+"
    },
    "%S": {
        "name": "bytes_transferred",
        "regex": r"\d+"
    },
    "%{Referer}i": {
        "name": "referer",
        "regex": r".*"
    },
    "%{User-Agent}i": {
        "name": "user_agent",
        "regex": r".*"
    }
}

token_types = {
    "bytes_received": int,
    "bytes_sent": int,
    "bytes_transferred": int,
    "canonical_port": int,
    "client_ip": str,
    "connection_status": None,
    "error_log_id": "clf",
    "filename": str,
    "final_status": int,
    "first_line": str,
    "handler": str,
    "hextid": None,
    "keepalive_count": int,
    "local_ip": str,
    "local_port": int,
    "pid": int,
    "pid_alt": int,
    "port": int,
    "query": str,
    "referer": str,
    "remote_hostname": str,
    "remote_logname": "clf_str",
    "remote_port": int,
    "remote_user": "clf_str",
    "request_method": str,
    "request_protocol": str,
    "response_size": int,
    "response_size_clf": "clf",
    "server_name": str,
    "server_name_ucn": str,
    "status": int,
    "tid": int,
    "time": None,
    "time_to_serve_s": int,
    "time_to_serve_us": int,
    "underlying_peer_ip": str,
    "underlying_remote_hostname": str,
    "url": str,
    "user_agent": str
}

def build_matcher(log_format):
    for token in tokens:
        log_format = log_format.replace(token, fr"(?P<{tokens[token]['name']}>{tokens[token]['regex']})", 1)
    return re.compile(log_format)

def match(matcher, line):
    if match := matcher.match(line):
        return {group: match.group(group) for group in matcher.groupindex}
    else:
        return None
