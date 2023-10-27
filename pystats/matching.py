import re

# "%v:%p %h %l %u %t \"%r\" %s:%>s %I %O \"%{Referer}i\" \"%{User-Agent}i\" %D %k %f \"%U\" \"%q\""
# %v:%p %h %l %u %t "%r" %s:%>s %I %O "%{Referer}i" "%{User-Agent}i" %D %k %f "%U" "%q"
# ^(\S+):(\d+) (\S+) (\S+) (\S+) (\[.+\]) "(.*)" (\d+):(\d+) (\d+) (\d+) "(.*)" "(.*)" (\d+) (\d+) (\S+) "(\S*)" "(\S*)"$

# "%v:%p %h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\" %a %A %b %B %D %f %H %k %L %m %P \"%U\" \"%q\" %R %T %V %X %I %S"
# %v:%p %h %l %u %t "%r" %>s %O "%{Referer}i" "%{User-Agent}i" %a %A %b %B %D %f %H %k %L %m %P "%U" "%q" %R %T %V %X %I %S
# ^(\S+):(\d+) (\S+) (\S+) (\S+) (\[.+\]) \"(.*)\" (\d+) (\d+) \"(.*)\" \"(.*)\" (\S+) (\S+) (-|\d+) (\d+) (\d+) (\S+) (\S+) (\d+) (-|\d+) (\S+) (\d+) \"(\S*)\" \"(\S*)\" (\S+) (\d+) (\S+) (X|\+|-) (\d+) (\d+)$

tokens = {
    r"%a": {
        "name": "client_ip",
        "regex": r"\S+"
    },
    r"%{c}a": {
        "name": "underlying_peer_ip",
        "regex": r"\S+"
    },
    r"%A": {
        "name": "local_ip",
        "regex": r"\S+"
    },
    r"%B": {
        "name": "response_size",
        "regex": r"\d+"
    },
    r"%b": {
        "name": "response_size_clf",
        "regex": r"-|\d+"
    },
    r"%D": {
        "name": "time_to_serve_us",
        "regex": r"\d+"
    },
    r"%f": {
        "name": "filename",
        "regex": r"\S+"
    },
    r"%h": {
        "name": "remote_hostname",
        "regex": r"\S+"
    },
    r"%{c}h": {
        "name": "underlying_remote_hostname",
        "regex": r"\S+"
    },
    r"%H": {
        "name": "request_protocol",
        "regex": r"\S+"
    },
    r"%k": {
        "name": "keepalive_count",
        "regex": r"\d+"
    },
    r"%l": {
        "name": "remote_logname",
        "regex": r"\S+"
    },
    r"%L": {
        "name": "error_log_id",
        "regex": r"-|\d+"
    },
    r"%m": {
        "name": "request_method",
        "regex": r"\S+"
    },
    r"%p": {
        "name": "port",
        "regex": r"\d+"
    },
    r"%{canonical}p": {
        "name": "canonical_port",
        "regex": r"\d+"
    },
    r"%{local}p": {
        "name": "local_port",
        "regex": r"\d+"
    },
    r"%{remote}p": {
        "name": "remote_port",
        "regex": r"\d+"
    },
    r"%P": {
        "name": "pid",
        "regex": r"\d+"
    },
    r"%{pid}P": {
        "name": "pid_alt",
        "regex": r"\d+"
    },
    r"%{tid}P": {
        "name": "tid",
        "regex": r"\d+"
    },
    r"%{hextid}P": {
        "name": "hextid",
        "regex": r"(?:0[xX])?[0-9a-fA-F]+"
    },
    r"%q": {
        "name": "query",
        "regex": r"\S*"
    },
    r"%r": {
        "name": "first_line",
        "regex": r".*"
    },
    r"%R": {
        "name": "handler",
        "regex": r"\S+"
    },
    r"%s": {
        "name": "status",
        "regex": r"\d+"
    },
    r"%>s": {
        "name": "final_status",
        "regex": r"\d+"
    },
    r"%t": {
        "name": "time",
        "regex": r"\[.+\]"
    },
    r"%T": {
        "name": "time_to_serve_s",
        "regex": r"\d+"
    },
    r"%u": {
        "name": "remote_user",
        "regex": r"\S+"
    },
    r"%U": {
        "name": "url",
        "regex": r"\S*"
    },
    r"%v": {
        "name": "server_name",
        "regex": r"\S+"
    },
    r"%V": {
        "name": "server_name_ucn",
        "regex": r"\S+"
    },
    r"%X": {
        "name": "connection_status",
        "regex": r"X|\+|-"
    },
    r"%I": {
        "name": "bytes_received",
        "regex": r"\d+"
    },
    r"%O": {
        "name": "bytes_sent",
        "regex": r"\d+"
    },
    r"%S": {
        "name": "bytes_transferred",
        "regex": r"\d+"
    },
    r"%{Referer}i": {
        "name": "referer",
        "regex": r".*"
    },
    r"%{User-Agent}i": {
        "name": "user_agent",
        "regex": r".*"
    },
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
