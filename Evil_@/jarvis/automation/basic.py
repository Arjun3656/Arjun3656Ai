import os
import sys

sys.path.insert(0, os.getcwd())

import webbrowser as web
from AppOpener import close, open as appopen  # Import functions to open and close apps.
from config import free_requests_session
from bs4 import BeautifulSoup

def google_search(topic: str) -> str:
    """Searches About the Topic on Google"""

    link = f"https://www.google.com/search?q={topic}"
    web.open(link)
    return f"{topic[:30]} has been searched on Google"

def youtube_search(Topic) -> str:
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"  # Construct the YouTube search URL.
    web.open(Url4Search)  # Open the search URL in a web browser.
    return f"{Topic[:30]} has been searched on YouTube"

# Function to open an application or a relevant webpage.
def open_app_or_website(app: str) -> str:
    sess = free_requests_session  # Create a session with free requests.

    try:
        appopen(app, match_closest=True, output=True, throw_error=True)  # Attempt to open the app.
        return f"Opening {app} app."  # Indicate success.
    
    except Exception:
        # Nested function to extract links from HTML content.
        def extract_links(html: str | None) -> list:
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')  # Parse the HTML content.
            links = soup.find_all('a', {'jsname': 'UWckNb'})  # Find relevant links.
            return [link.get('href') for link in links]  # Return the links.

        # Nested function to perform a Google search and retrieve HTML.
        def search_google(query: str) -> str:
            url = f"https://www.google.com/search?q={query}"  # Construct the Google search URL.
            headers = {
                "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
            }  # Use the predefined user-agent.
            response = sess.get(url, headers=headers)  # Perform the GET request.

            if response.status_code == 200:
                return response.text  # Return the HTML content.
            else:
                print("Failed to retrieve search results.")  # Print an error message.

        html = search_google(app)  # Perform the Google search.

        if html:
            link: str = extract_links(html)[0]  # Extract the first link from the search results.
            web.open(link)  # Open the link in a web browser.
            
            return f"Opening {app} website."  # Indicate success.
        return f"Could find {app} app or website."


def close_app(app) -> str:
    if "chrome" in app:
        pass  # Skip if the app is Chrome.
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)  # Attempt to close the app.
            return f"Closing {app}."  # Indicate success.
        except Exception:
            return f"Failed to close {app}."  # Indicate failure.


