
from rich.console import Console

from lib.dzr import Dzr

dzr = Dzr()

console = Console()

with open('songs.txt', 'r') as f:
    data = f.read().splitlines()

with console.status("Downloading...", spinner="line") as console:
    with open('links.txt', 'w') as f:
        for d in data:
            console.update(f"Retrieving link {d}")
            search = dzr.search(query=d)
            if search is not None:
                f.write(f"{search}\n")
    console.stop()


dzr.download(
    "links.txt",
    "FLAC"
)

console.update("Downloaded all songs!")
