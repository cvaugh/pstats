import analysis
import matching
import output
import parsing
from config import config
from pprint import pprint
from tqdm import tqdm
import pickle

def parse_log(matcher, lines):
    pbar = tqdm(lines, leave=False)
    pbar.set_description("Parsing lines")
    out = []
    for line in pbar:
        if matched := matching.match(matcher, line):
            out.append(parsing.parse(matched))
    pbar.close()
    return out

#log_format = "%v:%p %h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\" %a %A %b %B %D %f %H %k %L %m %P \"%U\" \"%q\" %R %T %V %X %I %S"

def main():
    matcher = matching.build_matcher(config["log_format"])

    #with open("TEST_temp.log", "r") as f:
    with open("merged.log", "r") as f:
        lines = [line.strip() for line in f.readlines()]
        parsed = parse_log(matcher, lines)
        #parsed = parse_log(matcher, lines[:5])

    if config["filter_loopback"]:
        parsed = [p for p in parsed if p["remote_hostname"] not in parsing._loopback_addresses]

    output_sections = analysis.get_valid_output_sections(parsed[0])
    analyzed = analysis.analyze(parsed, output_sections)
    output_sections.append("generated_date")
    generated = output.generate(analyzed, output_sections)
    output.write(generated)

#main()

with open("generated.dat", "rb") as f:
    generated = pickle.load(f)
