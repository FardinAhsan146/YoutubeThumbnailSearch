import requests
from PIL import Image
from io import BytesIO

def get_image_from_url(url: str) -> Image.Image:
    """
    Fetches an image from a given URL and returns it as a Pillow Image object.
    
    Args:
    url (str): The URL of the image to fetch.
    
    Returns:
    Image.Image: A Pillow Image object of the fetched image.
    
    Raises:
    requests.RequestException: If there's an error fetching the image.
    PIL.UnidentifiedImageError: If the fetched data cannot be identified as an image.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        image = Image.open(BytesIO(response.content))
        return image
    except requests.RequestException as e:
        print(f"Error fetching the image: {e}")
        raise
    except Image.UnidentifiedImageError:
        print("The fetched data could not be identified as an image.")
        raise
