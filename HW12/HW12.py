# from mistralai import Mistral
# from pyexpat.errors import messages
# import requests
# from settings import MISTRAL_API_KEY
# import base64
#
# class TextRequest:
#     def __init__(self, api_key):
#         self.api_key = api_key
#         self.base_url = "https://api.mistral.ai/v1/chat/completions"
#         self.headers = {
#             "Authorization": f"Bearer {api_key}",
#             "Content-Type": "application/json"
#         }
#
#     def send(self, messages:str):
#         client = Mistral(api_key=self.api_key)
#
#         payload = {
#             "model": "mistral-large-latest",
#             "messages": messages
#         }
#
#         try:
#             response = requests.post(self.base_url, headers=self.headers, json=payload)
#             response.raise_for_status()
#             return response.json()["choices"][0]["message"]["content"]
#         except requests.exceptions.RequestException as e:
#             print(f"Ошибка при отправке запроса: {e}")
#             return None
#         except KeyError as e:
#             print(f"Ошибка в структуре ответа: {e}")
#             return None
#
# class ImageRequest:
#     def __init__(self, api_key):
#         self.api_key = api_key
#         self.base64_img = None
#
#     def encode_image(self, image_pth):
#         """Encode the image to base64."""
#         try:
#             with open(image_pth, "rb") as image_file:
#                 self.base64_img = base64.b64encode(image_file.read()).decode('utf-8')
#                 return self.base64_img
#         except FileNotFoundError:
#             print(f"Error: The file {image_pth} was not found.")
#             return None
#         except Exception as e:  # Added general exception handling
#             print(f"Error: {e}")
#             return None
#
#     def send(self, messages, text: str, image_path: str):
#
#         # # Specify model
#         # model = "pixtral-12b-2409"
#         #
#         # # Initialize the Mistral client
#         # client = Mistral(api_key=self.api_key)
#         #
#         # # Define the messages for the chat
#         # messages = [
#         #     {
#         #         "role": "user",
#         #         "content": [
#         #             {
#         #                 "type": "text",
#         #                 "text": f"{text}"
#         #             },
#         #             {
#         #                 "type": "image_url",
#         #                 "image_url": f"data:image/jpeg;base64,{self.base64_img}"
#         #             }
#         #         ]
#         #     }
#         # ]
#         #
#         # # Get the chat response
#         # chat_response = client.chat.complete(
#         #     model=model,
#         #     messages=messages
#         # )
#         #
#         # # Print the content of the response
#         # print(chat_response.choices[0].message.content)
#
#
#
# class ChatFacade:
#
#     def __init__(self, api_key: str):
#         self.api_key = api_key
#         self.base_url = "https://api.mistral.ai/v1/chat/completions"
#         self.headers = {
#             "Authorization": f"Bearer {api_key}",
#             "Content-Type": "application/json"
#         }
#
#     def encode_image(self, image_path: str):
#         """Кодирует изображение в base64."""
#         try:
#             with open(image_path, "rb") as image_file:
#                 return base64.b64encode(image_file.read()).decode('utf-8')
#         except FileNotFoundError:
#             print(f"Ошибка: Файл {image_path} не найден.")
#             return None
#         except Exception as e:
#             print(f"Ошибка: {e}")
#             return None
#
#     def send(self, messages, image_path: str):
#         base64_image = self.encode_image(image_path)
#         if not base64_image:
#             return None
#
#         # Добавляем изображение к последнему сообщению пользователя
#         if messages and messages[-1]["role"] == "user":
#             messages[-1]["content"] = [
#                 {"type": "text", "text": messages[-1]["content"]},
#                 {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
#             ]
#
#         payload = {
#             "model": "mistral-large-latest",
#             "messages": messages
#         }
#
#         try:
#             response = requests.post(self.base_url, headers=self.headers, json=payload)
#             response.raise_for_status()
#             return response.json()["choices"][0]["message"]["content"]
#         except requests.exceptions.RequestException as e:
#             print(f"Ошибка при отправке запроса: {e}")
#             return None
#         except KeyError as e:
#             print(f"Ошибка в структуре ответа: {e}")
#             return None
#     # def __init__(self, api_key: str):
#     #     self.api_key = api_key
#     #     self.txtRequest = TextRequest(self.api_key)
#     #     self.imgRequest = ImageRequest(self.api_key)
#     #     self.mode = 1
#     #     self.messages = list[tuple[str, dict]]
#     #
#     # def select_mode(self, mode: int):
#     #     self.mode = mode
#     #     # return self.mode
#     #
#     # def load_image(self, image_path: str):
#     #     return self.imgRequest.encode_image(image_path)
#     #
#     # def ask_question(self, text: str, image_path: str = None):
#     #     if self.mode == 1:
#     #         return print(self.txtRequest.send(text))
#     #     else:
#     #         return print(self.imgRequest.send(text, image_path))
#     def __init__(self, api_key: str):
#         self.api_key = api_key
#         self.txtRequest = TextRequest(self.api_key)
#         self.imgRequest = ImageRequest(self.api_key)
#         self.messages = []  # История сообщений
#         self.mode = 1  # 1 - текст, 2 - изображение
#
#     def select_mode(self):
#         """Выбор режима работы."""
#         print("\nВыберите режим:")
#         print("1 - Текстовый чат")
#         print("2 - Анализ изображения")
#
#         while True:
#             try:
#                 mode = int(input("Введите номер режима (1 или 2): "))
#                 if mode in [1, 2]:
#                     self.mode = mode
#                     return mode
#                 else:
#                     print("Пожалуйста, введите 1 или 2")
#             except ValueError:
#                 print("Пожалуйста, введите число")
#
#     def add_message(self, role: str, content: str):
#         """Добавляет сообщение в историю."""
#         self.messages.append({"role": role, "content": content})
#
#     def display_history(self):
#         """Отображает историю сообщений."""
#         if not self.messages:
#             print("История пуста")
#             return
#
#         print("\n=== История чата ===")
#         for msg in self.messages:
#             role = "Вы" if msg["role"] == "user" else "Mistral"
#             content = msg["content"]
#             if isinstance(content, list):
#                 # Если содержимое - список (с изображением), показываем только текст
#                 text_content = next((item["text"] for item in content if item["type"] == "text"), "")
#                 print(f"{role}: {text_content} [+ изображение]")
#             else:
#                 print(f"{role}: {content}")
#         print("==================\n")
#
#     def ask_question(self, text: str, image_path: str = None):
#         """Отправляет вопрос и получает ответ."""
#         # Добавляем сообщение пользователя в историю
#         self.add_message("user", text)
#
#         if self.mode == 1:
#             # Текстовый режим
#             response = self.txtRequest.send(self.messages)
#         else:
#             # Режим с изображением
#             if not image_path:
#                 print("Для режима анализа изображения необходимо указать путь к файлу")
#                 return None
#             response = self.imgRequest.send(self.messages.copy(), image_path)
#
#         if response:
#             # Добавляем ответ ассистента в историю
#             self.add_message("assistant", response)
#             return response
#
#         return None
#
#     def start_chat(self):
#         """Запускает интерактивный чат."""
#         print("Добро пожаловать в чат с Mistral AI!")
#         print("Для завершения работы введите 'end'")
#         print("Для просмотра истории введите 'history'")
#         print("Для смены режима введите 'mode'")
#
#         # Выбираем начальный режим
#         self.select_mode()
#
#         while True:
#             user_input = input(f"\n[Режим {'Текст' if self.mode == 1 else 'Изображение'}] Ваш вопрос: ").strip()
#
#             if user_input.lower() == 'end':
#                 print("До свидания!")
#                 break
#             elif user_input.lower() == 'history':
#                 self.display_history()
#                 continue
#             elif user_input.lower() == 'mode':
#                 self.select_mode()
#                 continue
#             elif not user_input:
#                 print("Пожалуйста, введите вопрос")
#                 continue
#
#             # Если режим изображения, запрашиваем путь к файлу
#             image_path = None
#             if self.mode == 2:
#                 image_path = input("Введите путь к изображению: ").strip()
#                 if not image_path:
#                     print("Путь к изображению не указан")
#                     continue
#
#             print("Отправляю запрос...")
#             response = self.ask_question(user_input, image_path)
#
#             if response:
#                 print(f"\nMistral AI: {response}")
#             else:
#                 print("Не удалось получить ответ. Попробуйте еще раз.")
#
#     # Пример использования
#
#
# if __name__ == "__main__":
#
#     chat = ChatFacade(MISTRAL_API_KEY)
#     chat.start_chat()
#
# # if __name__ == "__main__":
# #     # text_request = TextRequest(MISTRAL_API_KEY)
# #     # text_request.send("Hello, how are you?", "mistral-large-latest")
# #
# #     # image_request = ImageRequest(MISTRAL_API_KEY)
# #     # image_request.send(r"C:\Users\Stark\Desktop\DR\We\We2.png")
# #
# #     # "Запустил фасад"
# #     chat = ChatFacade(MISTRAL_API_KEY)
# #
# #     # Выбираю режим
# #     chat.select_mode(2)
# #
# #     # Выбираю картинку
# #     chat.load_image(r"C:\Users\Stark\Desktop\DR\We\We2.png")
# #
# #     # Отправляю запрос и получаю ответ
# #     chat.ask_question("Привет, что ты видишь на фото?")
#
#
#

import base64
import requests
import json
import os
from settings import MISTRAL_API_KEY

class TextRequest:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.mistral.ai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def send(self, messages):
        payload = {
            "model": "mistral-large-latest",
            "messages": messages
        }

        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при отправке запроса: {e}")
            return None
        except KeyError as e:
            print(f"Ошибка в структуре ответа: {e}")
            return None


class ImageRequest:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.mistral.ai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def encode_image(self, image_path: str):
        """Кодирует изображение в base64."""
        try:
            # Проверяем существование файла
            if not os.path.exists(image_path):
                print(f"Ошибка: Файл {image_path} не найден.")
                return None

            # Проверяем формат файла
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
            file_extension = os.path.splitext(image_path.lower())[1]
            if file_extension not in valid_extensions:
                print(f"Ошибка: Неподдерживаемый формат файла. Поддерживаются: {', '.join(valid_extensions)}")
                return None

            with open(image_path, "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode('utf-8')
                print(f"Изображение успешно закодировано (размер: {len(encoded)} символов)")
                return encoded
        except FileNotFoundError:
            print(f"Ошибка: Файл {image_path} не найден.")
            return None
        except Exception as e:
            print(f"Ошибка при кодировании изображения: {e}")
            return None

    def send(self, messages, image_path: str):
        base64_image = self.encode_image(image_path)
        if not base64_image:
            return None

        # Определяем MIME тип изображения
        file_extension = os.path.splitext(image_path.lower())[1]
        mime_type = "image/jpeg"  # по умолчанию
        if file_extension == '.png':
            mime_type = "image/png"
        elif file_extension == '.gif':
            mime_type = "image/gif"
        elif file_extension == '.webp':
            mime_type = "image/webp"

        # Создаем новый список сообщений для этого запроса
        request_messages = []

        # Копируем все предыдущие сообщения (кроме последнего пользовательского)
        for msg in messages[:-1]:
            request_messages.append(msg)

        # Добавляем последнее сообщение пользователя с изображением
        if messages and messages[-1]["role"] == "user":
            user_message = {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": messages[-1]["content"]
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}"
                        }
                    }
                ]
            }
            request_messages.append(user_message)

        payload = {
            "model": "pixtral-12b-2409",  # Используем модель, поддерживающую изображения
            "messages": request_messages,
            "max_tokens": 1000
        }

        try:
            print("Отправляю запрос с изображением...")
            response = requests.post(self.base_url, headers=self.headers, json=payload)

            # Выводим детали ошибки для отладки
            if response.status_code != 200:
                print(f"Статус код: {response.status_code}")
                print(f"Ответ сервера: {response.text}")
                return None

            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при отправке запроса: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Детали ошибки: {e.response.text}")
            return None
        except KeyError as e:
            print(f"Ошибка в структуре ответа: {e}")
            return None


class ChatFacade:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.txtRequest = TextRequest(self.api_key)
        self.imgRequest = ImageRequest(self.api_key)
        self.messages = []  # История сообщений
        self.mode = 1  # 1 - текст, 2 - изображение

    def select_mode(self):
        """Выбор режима работы."""
        print("\nВыберите режим:")
        print("1 - Текстовый чат")
        print("2 - Анализ изображения")

        while True:
            try:
                mode = int(input("Введите номер режима (1 или 2): "))
                if mode in [1, 2]:
                    self.mode = mode
                    return mode
                else:
                    print("Пожалуйста, введите 1 или 2")
            except ValueError:
                print("Пожалуйста, введите число")

    def add_message(self, role: str, content: str):
        """Добавляет сообщение в историю."""
        self.messages.append({"role": role, "content": content})

    def display_history(self):
        """Отображает историю сообщений."""
        if not self.messages:
            print("История пуста")
            return

        print("\n=== История чата ===")
        for msg in self.messages:
            role = "Вы" if msg["role"] == "user" else "Mistral"
            content = msg["content"]
            if isinstance(content, list):
                # Если содержимое - список (с изображением), показываем только текст
                text_content = next((item["text"] for item in content if item["type"] == "text"), "")
                print(f"{role}: {text_content} [+ изображение]")
            else:
                print(f"{role}: {content}")
        print("==================\n")

    def ask_question(self, text: str, image_path: str = None):
        """Отправляет вопрос и получает ответ."""
        # Добавляем сообщение пользователя в историю
        self.add_message("user", text)

        if self.mode == 1:
            # Текстовый режим
            response = self.txtRequest.send(self.messages)
        else:
            # Режим с изображением
            if not image_path:
                print("Для режима анализа изображения необходимо указать путь к файлу")
                return None
            response = self.imgRequest.send(self.messages.copy(), image_path)

        if response:
            # Добавляем ответ ассистента в историю
            self.add_message("assistant", response)
            return response

        return None

    def start_chat(self):
        """Запускает интерактивный чат."""
        print("Добро пожаловать в чат с Mistral AI!")
        print("Для завершения работы введите 'end'")
        print("Для просмотра истории введите 'history'")
        print("Для смены режима введите 'mode'")
        print("Для очистки истории введите 'clear'")

        # Выбираем начальный режим
        self.select_mode()

        while True:
            try:
                user_input = input(f"\n[Режим {'Текст' if self.mode == 1 else 'Изображение'}] Ваш вопрос: ").strip()

                if user_input.lower() == 'end':
                    print("До свидания!")
                    break
                elif user_input.lower() == 'history':
                    self.display_history()
                    continue
                elif user_input.lower() == 'mode':
                    self.select_mode()
                    continue
                elif user_input.lower() == 'clear':
                    self.messages = []
                    print("История очищена")
                    continue
                elif not user_input:
                    print("Пожалуйста, введите вопрос")
                    continue

                # Если режим изображения, запрашиваем путь к файлу
                image_path = None
                if self.mode == 2:
                    image_path = input("Введите путь к изображению: ").strip()
                    if not image_path:
                        print("Путь к изображению не указан")
                        continue

                    # Убираем кавычки, если они есть
                    image_path = image_path.strip('"\'')

                print("Отправляю запрос...")
                response = self.ask_question(user_input, image_path)

                if response:
                    print(f"\nMistral AI: {response}")
                else:
                    print("Не удалось получить ответ. Попробуйте еще раз.")

            except KeyboardInterrupt:
                print("\n\nПрограмма прервана пользователем. До свидания!")
                break
            except Exception as e:
                print(f"Произошла ошибка: {e}")
                print("Попробуйте еще раз.")


# Пример использования
if __name__ == "__main__":


    chat = ChatFacade(MISTRAL_API_KEY)
    chat.start_chat()

