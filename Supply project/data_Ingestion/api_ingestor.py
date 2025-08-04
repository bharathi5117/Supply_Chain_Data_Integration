import requests

FAKE_STORE_API_URL = "https://fakestoreapi.com/products"

def fetch_fake_store_products():
    """
    Fetch product data from Fake Store API.

    Returns:
        list: List of product dictionaries
    """
    try:
        response = requests.get(FAKE_STORE_API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise Exception(f"API fetch failed: {e}")
