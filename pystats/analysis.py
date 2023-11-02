import _sections
import time
from config import config
from datetime import datetime
from tqdm import tqdm

output_sections = {
    "overall": {
        "required": ["remote_hostname", "bytes_sent"],
        "function": _sections.overall
    },
    "dates": {
        "required": ["time"],
        "function": _sections.dates
    },
    "bytes_transferred": {
        "required": ["bytes_sent", "bytes_received"],
        "function": _sections.bytes_transferred
    },
    "servers_table": {
        "required": ["time", "server_name", "bytes_sent"],
        "function": _sections.servers
    },
    "ports_table": {
        "required": ["time", "port", "bytes_sent"],
        "function": _sections.ports
    },
    "yearly_table": {
        "required": ["time", "bytes_sent", "remote_hostname"],
        "function": _sections.yearly
    },
    "monthly_table": {
        "required": ["time", "bytes_sent", "remote_hostname"],
        "function": _sections.monthly
    },
    "day_of_week_table": {
        "required": ["time", "bytes_sent", "remote_hostname"],
        "function": _sections.day_of_week
    },
    "hourly_table": {
        "required": ["time", "bytes_sent", "remote_hostname"],
        "function": _sections.hourly
    },
    "ip_table": {
        "required": ["time", "bytes_sent", "remote_hostname"],
        "function": _sections.ips
    },
    "users_table": {
        "required": ["time", "bytes_sent", "remote_user"],
        "function": _sections.users
    },
    "user_agent_table": {
        "required": ["time", "bytes_sent", "user_agent"],
        "function": _sections.user_agents
    },
    "files_table": {
        "required": ["time", "filename", "bytes_sent"],
        "function": _sections.files
    },
    "queries_table": {
        "required": ["query"],
        "function": _sections.queries
    },
    "referers_table": {
        "required": ["referer"],
        "function": _sections.referers
    },
    "responses_table": {
        "required": ["time", "final_status", "bytes_sent"],
        "function": _sections.responses
    },
    "time_taken_table": {
        "required": ["time_to_serve_us"],
        "function": _sections.time_taken
    }
}

def get_valid_output_sections(sample):
    valid = []
    for key in output_sections.keys():
        if all(i in sample.keys() for i in output_sections[key]["required"]):
            valid.append(key)
    return valid

def analyze(entries, valid_sections):
    data = {}
    _sections.entries = entries
    pbar = tqdm(valid_sections, leave=False)
    for section in pbar:
        pbar.set_description(section)
        data[section] = output_sections[section]["function"]()
    pbar.close()
    data["generated_date"] = { "date": datetime.fromtimestamp(int(time.time())) }
    return data
