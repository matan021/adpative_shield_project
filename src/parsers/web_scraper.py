import logging

import requests
from requests import Response
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


class WebScraper:
    """
    WebScraper is a utility class for fetching data from a given URL.

    Methods:
    --------
    fetch_data_from_url(url: str) -> Response:
        Fetches data from the given URL and returns the response. Raises an exception if the request fails.
    """

    @staticmethod
    def fetch_data_from_url(url: str) -> Response:
        """
        Fetch data from the given URL.

        Parameters:
        -----------
        url : str
            The URL to fetch data from.

        Returns:
        --------
        Response
            The response object containing the server's response to the HTTP request.

        Raises:
        -------
        RequestException
            If there is an issue with the network request.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
            return response
        except RequestException as e:
            logger.error(f"An error occurred while fetching data from the URL: {e}")
            raise  # Re-raise the caught exception
