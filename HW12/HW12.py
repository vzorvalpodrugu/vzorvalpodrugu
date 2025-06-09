from mistralai import Mistral
from settings import MISTRAL_API_KEY
import base64

class TextRequest:
    def __init__(self, api_key):
        self.api_key = api_key

    def send(self, text:str, model: str):
        client = Mistral(api_key=self.api_key)

        chat_response = client.chat.complete(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": f"{text}",
                },
            ]
        )
        print(chat_response.choices[0].message.content)

class ImageRequest:
    def __init__(self, api_key):
        self.api_key = api_key

    def send(self, image_path: str):
        def encode_image(image_pth):
            """Encode the image to base64."""
            try:
                with open(image_pth, "rb") as image_file:
                    return base64.b64encode(image_file.read()).decode('utf-8')
            except FileNotFoundError:
                print(f"Error: The file {image_pth} was not found.")
                return None
            except Exception as e:  # Added general exception handling
                print(f"Error: {e}")
                return None


        # Getting the base64 string
        base64_image = encode_image(image_path)

        # Specify model
        model = "pixtral-12b-2409"

        # Initialize the Mistral client
        client = Mistral(api_key=self.api_key)

        # Define the messages for the chat
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Что видишь на фото?"
                    },
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{base64_image}"
                    }
                ]
            }
        ]

        # Get the chat response
        chat_response = client.chat.complete(
            model=model,
            messages=messages
        )

        # Print the content of the response
        print(chat_response.choices[0].message.content)


if __name__ == "__main__":
    # text_request = TextRequest(MISTRAL_API_KEY)
    # text_request.send("Hello, how are you?", "mistral-large-latest")

    image_request = ImageRequest(MISTRAL_API_KEY)
    image_request.send(r"C:\Users\Stark\Desktop\DR\We\We2.png")