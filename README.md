# deezDownload

`deezDownload` is a wrapper around the [deemix](https://pypi.org/project/deemix/) Python executable. Currently, it takes in a song file based on the `%trackname% - %artistname%` and saves the files in the pre-defined [music](./music/) directory. 

## TODO

- [x] Upload to GitHub
- [ ] Add more song services (Spotify, YouTube...)
- [x] Make it in a more aesthetic manner (potential TUI?)
- [x] Make the code very sexy, readable and easy to modify

## Requirements

To use this tool, download the [requirements](./requirements.txt) in either a virtual environment or in your global Python installation. I recommend the virtual environment stance.

### venv

I used [uv's venv](https://github.com/astral-sh/uv) to manage and install my packages + it's insanely fast!

```bash
$ uv venv
$ .\venv\Scripts\activate
$ uv pip install -r requirements.txt
```

## Licencing

This program, "deezDownload" is protected by the MIT licence. Please familiarise yourself with it in the [LICENCE](./LICENCE) file.

## Credits

This tool has been created by Taran Nagra. I do not claim rights to this name `deezDownload`.

If you like this tool or have used it for your downloading needs, please say your thanks with a star ⭐!
