import matching
from pprint import pprint

with open("merged.log", "r") as f:
    lines = [line.strip() for line in f.readlines()]

log_format = "%v:%p %h %l %u %t \"%r\" %s:%>s %I %O \"%{Referer}i\" \"%{User-Agent}i\" %D %k %f \"%U\" \"%q\""

matcher = matching.build_matcher(log_format)

pprint(matching.match(matcher, lines[-1]))
