import os
import rich
import requests
from rich.console import Console

class Dzr:
    def __init__(self) -> None:
        self.console = Console()
        self.session = requests.Session()

        self.search_url = "https://api.deezer.com/search?q={}&output=json&output=json&version=js-v1.0.0"

        self.download_query = "deemix --portable {} --path ./music/ --bitrate {} > NUL "

    def search(self, query: str) -> str:
        """
            Searches the Deezer API and returns the 1st link.
            Args:
                - query -> Should be in the format:
                    - %track% %artist%
        """
        r = self.session.get(
            url=self.search_url.format(query.replace(" ", "%20"))
        )
        if r.status_code == 200:
            try:
                return r.json()["data"][0]["link"]
            except IndexError:
                print(f"Song: {query} could not be found!")
                return
        raise Exception(f"Failed to make a request: {r.status_code}")
    
    def download(self, song_file: str, bitrate: str = "FLAC") -> str:
        """Downloads the song by the link using Deemix"""
        x = 1
        with open(song_file, 'r') as f:
            links = f.read().splitlines()
        with self.console.status("Downloading...", spinner="line") as status:
            for link in links:
                if not link == "":
                    status.update(f"Downloading song {x} of {len(links)}...")
                    os.system(
                        self.download_query.format(
                            link,
                            bitrate
                        )
                    )
                    status.update(f"Downloaded {link}!")
                    x += 1
        rich.print("[bold green]Downloaded all songs!")
    
    def init(self) -> None:
        """Initialises the directory for Deemix using a sample song."""
        os.system(
            "deemix --portable https://www.deezer.com/track/2817137262 --path ./music/ --bitrate FLAC > NUL"
        )
