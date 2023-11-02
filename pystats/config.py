config = {
    "log_format": "%v:%p %h %l %u %t \"%r\" %s:%>s %I %O \"%{Referer}i\" \"%{User-Agent}i\" %D %k %f \"%U\" \"%q\"",
    "date_format": "%Y-%m-%d %H:%M:%S %z",
    "page_title": "Apache Statistics",
    "output_directory": "./out",
    "use_si_units": True,
    "whois_tool": "https://iplocation.io/ip/{{address}}",
    "filter_loopback": True,
    "time_taken_buckets": [100, 500, 1000, 5000, 10000, 50000],
    "truncate": 100,
    "visit_thresholds": {
        "ip_table": 50,
        "user_agent_table": 50,
        "users_table": 0,
        "files_table": 0,
        "queries_table": 0,
        "referers_table": 0
    }
}
