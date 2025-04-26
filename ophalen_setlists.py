from pathlib import Path
import requests
import os
from dotenv import load_dotenv

load_dotenv()


def haal_op_setlists():
    res = requests.get(
        "https://api.setlist.fm/rest/1.0/user/Tijmen_31/attended?p=1",
        headers={
            "x-api-key": os.environ["SETLIST_API_KEY"],
            "Accept": "application/json",
        }
    )
    return res.json()


def maak_html_widgets(setlists: dict):
    widgets = ""

    for setlist in setlists["setlist"]:
        # Sets zonder nummers overslaan
        if setlist["sets"] == {"set": []}:
            continue

        setlist_url = setlist["url"]
        setlist_id = setlist["id"]
        widget_url = (
            f"https://www.setlist.fm/widgets/setlist-image-v1"
            f"?id={setlist_id}&font=1&bg=eff5ef"
        )
        widgets += (
            f'<div style="text-align: center;" class="setlistImage"'
            f' href="{setlist_url}">\n'
            f'  <a target="_blank"><img src="{widget_url}" style="border: 0;"'
            f' /></a>\n</div>'
        )
    return widgets


def verwerk_html_sjabloon(widgets: str):
    sjabloon = Path("sjabloon.html").read_text()
    html = sjabloon.replace("---voeg setlists hier toe---", widgets)
    with open("verwerkt.html", "w") as website:
        website.write(html)


if __name__ == "__main__":
    setlists = haal_op_setlists()
    widgets = maak_html_widgets(setlists)
    verwerk_html_sjabloon(widgets)
