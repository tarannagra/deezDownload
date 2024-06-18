"""
dzr.py - A module for searching and downloading songs from Deezer using Deemix.

Copyright (c) Taran Nagra 2024

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

"""

import os
import asyncio

import requests

from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Horizontal
from textual.widgets import (
    Header, 
    Footer, 
    Button, 
    Label,
    ProgressBar
)


class Dzr:
    """
    Deezer download class to search and download the songs.
    """
    def __init__(self) -> None:
        self.session = requests.Session()
        self.bitrate = "FLAC"

        self.search_url = "https://api.deezer.com/search?q={}&output=json&output=json&version=js-v1.0.0"

        self.download_query = "deemix --portable {} --path ./music/ --bitrate {} > NUL "
    
    def clean(self) -> None:
        """
        Removes all media files from the music path and their respective file extension.
        
        Args:
            None
            
        Returns:
            None
        
        """
        os.system(f"rm ./music/*.{self.bitrate.lower()}")

    def search(self, query: str) -> str:
        """
        Searches the Deezer API using the provided query and returns the first link found.

        Args:
            query (str): The search query in the format "%track% %artist%".

        Returns:
            str: The Deezer link of the first search result.

        Raises:
            Exception: If the request to the Deezer API fails.
        """
        r = self.session.get(
            url=self.search_url.format(query.replace(" ", "%20"))
        )
        if r.status_code == 200:
            try:
                return r.json()["data"][0]["link"]
            except IndexError:
                return None
        raise Exception(f"Failed to make a request: {r.status_code}")
    
    async def download(self, song_link: str, bitrate: str = "FLAC") -> None:
        """
        Asynchronously downloads the song by the link using Deemix.

        Args:
            song_link (str): The given track link returned from `self.search()`.
            bitrate (str): The bitrate in which to download the music in. Defaults to FLAC.
        
        Returns:
            None
        
        
        """
        self.bitrate = bitrate
        await asyncio.to_thread(os.system, self.download_query.format(song_link, bitrate))
    
    def init(self) -> None:
        """Initialises the directory for Deemix using a sample song."""
        os.system(
            "deemix --portable https://www.deezer.com/track/2817137262 --path ./music/ --bitrate FLAC > NUL"
        )

dzr = Dzr()

class DownloadScreen(Screen):
    """
    DownloadScreen class to handle the new Screen to be added in the main file.
    Can be replaced and ran as own executable file, but this is better file management - for me.
    """
    def compose(self) -> ComposeResult:
        """
        Starting point for this TUI to render a visual for the user to click about in.

        Args:
            None
        
        Returns:
            ComposeResult
        """
        self.links = []
        yield Header()
        yield Container(
            Horizontal(
                Button("Load song file!", variant="primary", id="load_links"),
                Button("Download songs!", variant="default", id="download_songs"),
                Button("CLEAN FOLDER!", variant="error", id="clean_folder"),
                classes="button-container"
            ),
            id="containers"
        )
        self.content = Label("Status: ...")
        self.progress_bar = ProgressBar(total=1, show_eta=True)
        yield Container(
            self.content,
            self.progress_bar,
            classes="status-container"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Determine the appropriate action based on the button pressed! 
        
        **Called as an event, not by the user.**
        
        Args:
            event (Button.Pressed): the button pressed.
        """
        
        if event.button.id == "load_links":
            self.content.update("Status: [yellow]Loading files...[/yellow]")
            self.links = self.search()
            if self.links is None:
                self.content.update("Status: [yellow]Songs file empty! Please add to it and re-run![/yellow]")
                return
        elif event.button.id == "download_songs":
            if len(self.links) == 0:
                self.content.update("Status: [red]I have no links! Please load some and then press this again![/red]")
            else:
                self.content.update("Status: [yellow]Downloading song(s)...")
                asyncio.create_task(self.download())
        elif event.button.id == "clean_folder":
            dzr.clean()
            self.content.update("[green]Status: Folder has been cleaned![/green]")
    
    async def download(self) -> None:
        """
        Asynchronous function to download the list of songs in `self.links`

        Args:
            None

        Returns:
            None
        """
        for song in self.links:
            await dzr.download(song)
            self.query_one(ProgressBar).advance(1)
        self.query_one(ProgressBar).update(total=len(self.links))
        self.content.update(f"Status: [green]Downloaded {len(self.links)} songs!")
                

    def search(self) -> list[str]:
        """
        Search function which taps into the Dzr() class to search songs based on the given songs file.

        Args:
            None

        Returns:
            None: only returns None if song file is empty and cannot continue.
            links (list[str]): list of available links found that best match the song.
        """
        links = []
        with open('songs.txt', 'r') as f:
            song_names = f.read().splitlines()
        if len(song_names) == 0:
            self.content.update("Status: [yellow]Songs file empty! Please add to it and re-run![/yellow]")
            return
        for song_name in song_names:
            result = dzr.search(query=song_name)
            if result is None:
                self.content.update(f"Status: [red]{song_name} could not be found![/red]")
            else:
                self.content.update(f"Status: [green]{song_name} found![/green]")
                links.append(result)
        self.content.update("Status: [green]Song(s) found! You can proceed to download them![/green]")
        self.progress_bar.update(total=len(links))
        return links

