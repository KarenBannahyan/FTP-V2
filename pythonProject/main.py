import socket
import os
from PIL import Image, ImageDraw, ImageFont
def get_server_ip():
    return socket.gethostbyname(socket.gethostname())
def get_new_photo_filename():
    photo_dir = "received_photos"
    existing_photos = [f for f in os.listdir(photo_dir) if
                       f.lower().startswith("received_photo") and f.lower().endswith(".jpg")]
    new_photo_number = len(existing_photos) + 1
    return os.path.join(photo_dir, f"received_photo{new_photo_number}.jpg")
def add_text_to_image(image_path, text):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 20)  # Замените "arial.ttf" на путь к вашему TTF-шрифту
    except IOError:
        font = ImageFont.load_default()  # Шрифт по умолчанию, если TTF не найден
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    width, height = image.size
    position = (width - text_width - 10, height - text_height - 10)
    draw.text(position, text, font=font, fill=(0, 0, 0))  # Используем черный цвет текста для контраста
    image.save(image_path)
def log_client_id(client_id):
    with open("client_ids.txt", "a") as log_file:
        log_file.write(f"{client_id}\n")
def main():
    port = int(input("Введите порт для сервера: "))
    server_ip = get_server_ip()
    print(f"IPv4 адрес сервера: {server_ip}")
    if not os.path.exists("received_photos"):
        os.makedirs("received_photos")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (server_ip, port)
    server_socket.bind(server_address)
    server_socket.listen(1)
    print("Сервер запущен, ожидание подключений...")
    while True:
        client_socket, client_address = server_socket.accept()
        client_id = client_address[0]
        print(f"Подключен клиент: {client_address}")
        photo_data = b""
        while True:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            photo_data += chunk
        photo_name = get_new_photo_filename()
        with open(photo_name, 'wb') as file:
            file.write(photo_data)
        add_text_to_image(photo_name, client_id)
        log_client_id(client_id)
        print(f"Фотография сохранена как {photo_name}")
        client_socket.close()
if __name__ == "__main__":
    main()
