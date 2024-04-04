import os
import tracemalloc
from telethon.sync import TelegramClient, functions
from dotenv import load_dotenv

tracemalloc.start()


class handler():
    def __init__(self) -> None:
        # Load variables from the .env file
        load_dotenv('config/config.env')

        # Access  key
        api_id = os.getenv('api_id')
        api_hash = os.getenv('api_hash')
        phone_number = os.getenv('phone_number')
        session_name = os.getenv('session_name')

        # Create a Telegram client
        self.client = TelegramClient(session_name, api_id, api_hash)

        # Connect to the Telegram servers
        self.client.connect()

        # If not authorized, send an authorization code request
        if not self.client.is_user_authorized():
            self.client.send_code_request(phone_number)

            code = input('Enter the code: ')

            try:
                # For accounts with two-step verification
                self.client.sign_in(phone_number, code)

            except Exception as e:
                # Handle the two-step verification exception

                password = input('Enter your Telegram password: ')
                self.client.sign_in(phone_number, password=password)

    def send_message(self, name, message):
        # Connect to the Telegram servers
        self.client.connect()

        # Search for users with the given name
        result = self.client(functions.contacts.SearchRequest(
            q=name,
            limit=10
        ))

        # Check if any users were found
        if result.users:
            # Assuming the first user in the result is the one you are looking for
            user = result.users[0]

            self.client.send_message(user, message=message)
            self.client.disconnect()
            return (f"I have sent the requested message to {user.first_name}")

        else:
            self.client.disconnect()
            return (f"Sorry, I could not find a user with the name '{name}'.")
