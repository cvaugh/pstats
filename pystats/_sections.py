from config import config
from datetime import datetime

entries = []
total_bandwidth = -1

si_prefixes = "KMGTPEZY"
month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
day_names = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

def format_bytes(b):
    n = 1000 if config["use_si_units"] else 1024
    if(b < n):
        return f"{b} B"
    i = -1
    while b > n:
        b /= n
        i += 1
    return f"{b:.02f} {si_prefixes[i]}{'' if config['use_si_units'] else 'i'}B"

def overall():
    return {
        "visitors": len(set([entry["remote_hostname"] for entry in entries])),
        "visits": len(entries),
        "bandwidth": format_bytes(sum([entry["bytes_sent"] for entry in entries]) + sum([entry["bytes_received"] for entry in entries]))
    }

def dates():
    dates = sorted([entry["time"] for entry in entries])
    return {
        "earliest": datetime.fromtimestamp(dates[0]),
        "latest": datetime.fromtimestamp(dates[-1])
    }

def bytes_transferred():
    sent = sum([entry["bytes_sent"] for entry in entries])
    received = sum([entry["bytes_received"] for entry in entries])
    return {
        "sent": format_bytes(sent),
        "received": format_bytes(received),
        "total": format_bytes(sent + received)
    }

def servers():
    return { "rows": get_uvbl("server_name") }

def ports():
    return { "rows": get_uvbl("port") }

def yearly():
    return get_time_averages(get_visits_by_time("%Y"))

def monthly():
    rows = get_visits_by_time("%b")
    new_rows = []
    for name in month_names:
        row = [row for row in rows if row["key"] == name]
        if len(row) > 0:
            new_rows.append(row[0])
    return get_time_averages(new_rows)

def day_of_week():
    rows = get_visits_by_time("%a")
    new_rows = []
    for name in day_names:
        row = [row for row in rows if row["key"] == name]
        if len(row) > 0:
            new_rows.append(row[0])
    return get_time_averages(new_rows)

def hourly():
    return get_time_averages(get_visits_by_time("%H"))

def ips():
    rows = []
    for row in get_vbl("remote_hostname"):
        rows.append({
            "key": row["key"],
            "whois": "<a class=\"whois\" href=\"" + config["whois_tool"].replace("{{address}}", row["key"]) + "\">View</a>",
            "visits": row["visits"],
            "visit_percentage": row["visit_percentage"],
            "bandwidth": row["bandwidth"],
            "banwidth_percentage": row["bandwidth_percentage"],
            "latest_visit": row["latest_visit"]
        })
    return { "rows": rows }

def users():
    return { "rows": get_uvbl("remote_user") }

def user_agents():
    return { "rows": get_uvbl("user_agent") }

def files():
    rows = []
    for row in get_uvbl("filename", do_byte_format=False):
        rows.append({
            "key": row["key"],
            "unique_visitors": row["unique_visitors"],
            "visits": row["visits"],
            "visit_percentage": row["visit_percentage"],
            "bandwidth": format_bytes(row["bandwidth"]),
            "bandwidth_percentage": row["bandwidth_percentage"],
            "average_bandwidth": format_bytes(round(row["bandwidth"] / row["visits"])),
            "latest_visit": row["latest_visit"]
        })
    return { "rows": rows }

def queries():
    return { "rows": get_uvbl("query") }

def referers():
    return { "rows": get_uvbl("referer") }

def responses():
    return { "rows": get_uvbl("final_status") }

def time_taken():
    rows = []
    for i in range(1, len(config["time_taken_buckets"])):
        rows.append({
            "key": str(config["time_taken_buckets"][i - 1]) + "&ndash;" + str(config["time_taken_buckets"][i]),
            "count": 0,
            "percentage": 0
        })
    rows.insert(0, {"key": f"< {config['time_taken_buckets'][0]}", "count": 0, "percentage": 0})
    rows.append({"key": f"&geq; {config['time_taken_buckets'][-1]}", "count": 0, "percentage": 0})
    for entry in entries:
        t = entry["time_to_serve_us"]
        if t < config["time_taken_buckets"][0]:
            rows[0]["count"] += 1
        elif t >= config["time_taken_buckets"][-1]:
            rows[-1]["count"] += 1
        for i in range(len(config["time_taken_buckets"])):
            if t < config["time_taken_buckets"][i]:
                rows[i]["count"] += 1
                break
    for row in rows:
        row["percentage"] = get_percentage(row["count"], len(entries))
    return { "rows": rows , "average": f"{sum([entry['time_to_serve_us'] for entry in entries]) / len(entries):.02f}"}

def get_uvbl(key, sort_by="visits", do_byte_format=True):
    values = {entry[key]: {
            "key": entry[key],
            "unique_visitors": 0,
            "visits": 0,
            "visit_percentage": 0,
            "bandwidth": 0,
            "bandwidth_percentage": 0,
            "latest_visit": 0
        } for entry in entries}
    remote_hosts = {}
    for entry in entries:
        values[entry[key]]["visits"] += 1
        values[entry[key]]["bandwidth"] += entry["bytes_sent"]
        if entry["time"] > values[entry[key]]["latest_visit"]:
            values[entry[key]]["latest_visit"] = entry["time"]
        if entry[key] not in remote_hosts:
            remote_hosts[entry[key]] = [entry["remote_hostname"]]
        else:
            remote_hosts[entry[key]].append(entry["remote_hostname"])
    values = [values[k] for k in values.keys()]
    values.sort(key=lambda x: x[sort_by], reverse=True)
    for value in values:
        value["unique_visitors"] = len(set(remote_hosts[value["key"]]))
        value["visit_percentage"] = get_percentage(value["visits"], len(entries))
        value["bandwidth_percentage"] = get_percentage(value["bandwidth"], get_total_bandwidth())
        value["bandwidth"] = format_bytes(value["bandwidth"]) if do_byte_format else value["bandwidth"]
        value["latest_visit"] = datetime.fromtimestamp(value["latest_visit"])
    return values

def get_vbl(key, sort_by="visits"):
    rows = get_uvbl(key, sort_by)
    for row in rows:
        del row["unique_visitors"]
    return rows

def get_visits_by_time(time_format):
    values = {}
    remote_hosts = {}
    for entry in entries:
        value = datetime.fromtimestamp(entry["time"]).strftime(time_format)
        if value not in values:
            values[value] = {
                "key": value,
                "unique_visitors": 0,
                "visits": 1,
                "visit_percentage": 0,
                "bandwidth": entry["bytes_sent"],
                "bandwidth_percentage": 0
            }
            remote_hosts[value] = [entry["remote_hostname"]]
        else:
            values[value]["visits"] += 1
            values[value]["bandwidth"] += entry["bytes_sent"]
            remote_hosts[value].append(entry["remote_hostname"])
    values = [values[k] for k in values.keys()]
    values.sort(key=lambda x: x["key"])
    for value in values:
        value["unique_visitors"] = len(set(remote_hosts[value["key"]]))
        value["visit_percentage"] = get_percentage(value["visits"], len(entries))
        value["bandwidth_percentage"] = get_percentage(value["bandwidth"], get_total_bandwidth())
        value["bandwidth"] = format_bytes(value["bandwidth"])
    return values

def get_total_bandwidth():
    global total_bandwidth
    if total_bandwidth < 0:
        for entry in entries:
            total_bandwidth += entry["bytes_sent"]
    return total_bandwidth

def get_percentage(part, whole):
    return f"{part * 100 / whole:0.02f}%"

def get_time_averages(rows):
    return {
        "rows": rows,
        "average_visitors": f"{sum([row['unique_visitors'] for row in rows]) / len(rows):.02f}",
        "average_visits": f"{len(entries) / len(rows):.02f}",
        "average_bandwidth": format_bytes(get_total_bandwidth() / len(rows))
    }
