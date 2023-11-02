import os
from config import config
from datetime import datetime
from sys import stderr
from tqdm import tqdm

def escape(s):
    return s # TODO

def truncate(s):
    return "<span class=\"truncated\" title=\"" + s + "\">" + s[:config["truncate"]] + "<span class=\"truncation-marker\">&raquo;</span></span>"

def format_cell(data):
    if data is datetime:
        s = datetime.strftime(data)
    else:
        s = escape(str(data))
    if config["truncate"] < 1:
        return s
    return s if len(s) <= config["truncate"] else truncate(s)

def generate_row(data):
    return "<tr>" + "".join(["<td>" + format_cell(i) + "</td>" for i in data]) + "</tr>"

def get_table_with_rows(template, data):
    rows = []
    for row in data["rows"]:
        rows.append(generate_row(tuple(row[i] for i in row)))
    data["rows"] = "\n".join(rows)
    return fill_template(template, data)

def get_template(name):
    with open(os.path.join(os.path.dirname(__file__), "resources", "templates", name + ".html"), "r") as f:
        lines = f.readlines()
    return "".join(lines)

def fill_template(template, data):
    if data is None:
        return # FIXME
    for key in data.keys():
        template = template.replace("{{" + key + "}}", str(data[key]))
    return template

def generate(analyzed, output_sections):
    templates = {}
    pbar = tqdm(output_sections, leave=False)
    for section in output_sections:
        pbar.set_description(section)
        template = get_template(section)
        if "rows" in analyzed[section].keys():
            if section in config["visit_thresholds"]:
                analyzed[section]["rows"] = [i for i in analyzed[section]["rows"] if i["visits"] >= config["visit_thresholds"][section]]
            templates[section] = get_table_with_rows(template, analyzed[section])
        else:
            templates[section] = fill_template(template, analyzed[section])
    pbar.close()
    templates["footer"] = get_template("footer")
    with open(os.path.join(os.path.dirname(__file__), "resources", "templates", "styles.css"), "r") as f:
        lines = f.readlines()
    templates["styles"] = "".join(lines)
    templates["page_title"] = config["page_title"]
    return templates

def write(filled_templates):
    template = get_template("main")
    for key in filled_templates.keys():
        template = template.replace("{{" + key + "}}", filled_templates[key])
    if not os.path.exists(config["output_directory"]):
        os.makedirs(config["output_directory"])
    elif os.path.isfile(config["output_directory"]):
        print("Error: Output directory may not be a file:", config["output_directory"], file=stderr)
    with open(os.path.join(config["output_directory"], "index.html"), mode="w", encoding="utf-8") as out:
        out.write(template)
