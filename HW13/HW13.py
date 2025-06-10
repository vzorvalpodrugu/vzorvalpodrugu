import base64
from logging import lastResort

import requests
import json
import os
from settings import MISTRAL_API_KEY
from abc import ABC, abstractmethod

class RequestStrategy(ABC):
    @abstractmethod
    def send(self, messages: str, history: list = None, image_path: str = None) -> dict:
        pass

class TextRequestStrategy(RequestStrategy):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.mistral.ai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def send(self, messages: str, history: list = None, image_path: str = None) -> dict:
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


class ImageRequestStrategy(RequestStrategy):
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

    def send(self, messages: str, history: list = None, image_path: str = None):
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
        self.txtRequest = TextRequestStrategy(self.api_key)
        self.imgRequest = ImageRequestStrategy(self.api_key)
        self.messages = []  # История сообщений
        self.strategy = 1  # 1 - текст, 2 - изображение

    def change_strategy(self):
        """Выбор стратегии"""
        print("\nВыберите стратегию:")
        print("1 - Текстовый чат")
        print("2 - Анализ изображения")

        while True:
            try:
                strategy = int(input("Введите номер стратегии (1 или 2): "))
                if strategy in [1, 2]:
                    self.strategy = strategy
                    return strategy
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

        if self.strategy == 1:
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
        print("Для смены стратегии введите 'strategy'")
        print("Для очистки истории введите 'clear'")

        # Выбираем начальный режим
        self.change_strategy()

        while True:
            try:
                user_input = input(f"\n[Стратегия {'Текст' if self.strategy == 1 else 'Изображение'}] Ваш вопрос: ").strip()

                if user_input.lower() == 'end':
                    print("До свидания!")
                    break
                elif user_input.lower() == 'history':
                    self.display_history()
                    continue
                elif user_input.lower() == 'strategy':
                    self.change_strategy()
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
                if self.strategy == 2:
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