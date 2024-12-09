import requests

def download_image(url, save_path):
    try:
        # Send a GET request to the image URL
        response = requests.get(url)
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()

        # Open a file in binary write mode and save the image
        with open(save_path, 'wb') as file:
            file.write(response.content)
        
        print(f"Image successfully downloaded and saved to {save_path}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

# Example usage
image_url = 'https://i.ibb.co/1LZq699/2.jpg'  # Replace with the actual URL
save_location = 'downloaded_image1.jpg'  # Local path to save the image
download_image(image_url, save_location)
