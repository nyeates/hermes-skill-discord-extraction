import csv
from datetime import datetime

inp = "raw.csv"
out = "clean.txt"

last_date = None

def format_date(date_text):
    date_text = date_text.strip().replace("Z", "+00:00")

    # DiscordChatExporter may output 7 fractional-second digits.
    # Python datetime only accepts 6.
    if "." in date_text:
        before_dot, after_dot = date_text.split(".", 1)

        for sep in ["+", "-"]:
            if sep in after_dot:
                frac, tz = after_dot.split(sep, 1)
                date_text = f"{before_dot}.{frac[:6]}{sep}{tz}"
                break
        else:
            date_text = f"{before_dot}.{after_dot[:6]}"

    dt = datetime.fromisoformat(date_text)
    return dt.strftime("%m/%d/%Y")

with open(inp, newline="", encoding="utf-8-sig") as f, open(out, "w", encoding="utf-8") as g:
    reader = csv.DictReader(f)

    for row in reader:
        day = format_date(row["Date"])

        if day != last_date:
            g.write(f"\n\n=== {day} ===\n\n")
            last_date = day

        author = row["Author"]
        content = row["Content"].strip()

        if content:
            g.write(f"{author}: {content}\n")
