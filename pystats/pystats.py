import matching
import parsing
from pprint import pprint

with open("TEST_temp.log", "r") as f:
    lines = [line.strip() for line in f.readlines()]

#log_format = "%v:%p %h %l %u %t \"%r\" %s:%>s %I %O \"%{Referer}i\" \"%{User-Agent}i\" %D %k %f \"%U\" \"%q\""
log_format = "%v:%p %h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\" %a %A %b %B %D %f %H %k %L %m %P \"%U\" \"%q\" %R %T %V %X %I %S"

matcher = matching.build_matcher(log_format)

log_elements = matching.match(matcher, lines[-1])

parsed_elements = parsing.parse(log_elements)

pprint(parsed_elements)
