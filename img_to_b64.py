# import base64

# def image_to_base64(image_path):
#     """
#     Converts an image to a base64 string.
    
#     :param image_path: Path to the image file
#     :return: Base64 encoded string of the image
#     """
#     try:
#         # Open image file in binary mode
#         with open(image_path, "rb") as image_file:
#             # Read the image file and encode it to base64
#             encoded_string = base64.b64encode(image_file.read())
#             return encoded_string.decode('utf-8')
#     except FileNotFoundError:
#         print(f"File {image_path} not found.")
#         return None

# if __name__ == "__main__":
#     # Example usage
#     image_path = 'test/1.jpg'  # Replace with your image path
#     base64_string = image_to_base64(image_path)
    
#     if base64_string:
#         print("Image successfully converted to Base64.")
#         print(base64_string)  # Optionally print or save the encoded string

import base64
import os

def image_to_base64(image_path):
    """
    Converts an image to a base64 string and saves it to a text file.
    
    :param image_path: Path to the image file
    """
    try:
        # Open image file in binary mode
        with open(image_path, "rb") as image_file:
            # Read the image file and encode it to base64
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

            # Generate the .txt file path
            base_filename = os.path.splitext(image_path)[0]  # Get the file name without extension
            txt_file_path = f"{base_filename}.txt"  # Add .txt extension

            # Save the base64 string to the text file
            with open(txt_file_path, "w") as txt_file:
                txt_file.write(encoded_string)
            
            print(f"Base64 string successfully saved to {txt_file_path}")
    except FileNotFoundError:
        print(f"File {image_path} not found.")

if __name__ == "__main__":
    # Example usage
    image_path = 'test/1.jpg'  # Replace with your image path
    image_to_base64(image_path)
