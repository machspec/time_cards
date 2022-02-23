"""Functions used to check for updates using the GitHub API"""

from app.constants import APP_VERSION, GITHUB_API_URL, GITHUB_RELEASES_URL

import requests
import webbrowser


def update_available() -> bool:
    """Check if the program version matches that of the latest release."""
    path = GITHUB_API_URL
    response = requests.get(path + "/latest")

    # in case only pre-releases available
    if response.json()["message"] == "Not Found":
        response = requests.get(path)

    return response.json()[0]["tag_name"] != APP_VERSION


def open_releases() -> None:
    """Open the Releases page of the program repo."""

    # tries to open a new tab, opens a new window if it can't
    webbrowser.open(GITHUB_RELEASES_URL, 2)
