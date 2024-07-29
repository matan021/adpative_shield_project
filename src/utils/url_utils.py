from urllib.parse import urljoin

def concat_url(base_url: str, path: str) -> str:
    """
    Concatenates a base URL with a path to form a complete URL.

    Parameters:
    base_url (str): The base URL.
    path (str): The path to be appended to the base URL.

    Returns:
    str: The complete URL formed by concatenating the base URL with the path.
    """
    return urljoin(base_url, path)