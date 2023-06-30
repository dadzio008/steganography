from tkinter.ttk import Entry

from PIL import Image
from tkinter import Tk, Label, Button, filedialog

# zmienne globalne wartosci scieżek
image_path = ""
encoded_image_path = ""


def encode_image():
    global image_path
    try:
        # Otwarcie obrazu
        image = Image.open(image_path)

        # Zaciagniecie wiadomosci
        secret_message = message_entry.get()

        # Sprawdzenie czy obraz ma tyle pikseli żeby umieścić w nim wiadomość
        max_size = image.width * image.height
        if len(secret_message) > max_size:
            raise ValueError("Wiadomość jest zbyt długa dla danego obrazu.")

        # Zamiana wiadomości na system binarny
        binary_message = ''.join(format(ord(c), '08b') for c in secret_message)

        # Kopiowanie obrazu
        encoded_image = image.copy()
        index = 0
        # Dla wartości szerokości obrazu
        for x in range(image.width):
            # Dla wartości wysokości obrazu
            for y in range(image.height):
                # Sprawdzenie czy wiadomości już została wstrzyknięta
                if index < len(binary_message):
                    # Pobranie pixela o wartościach x,y
                    pixel = list(image.getpixel((x, y)))
                    #Ustawia trzeci pixel jako (najmniej znaczacy bit jako 0 w kazdym przypadku a nastepnie porownuje z wiadomoscia i ustawia 1 gdzie tak powinno byc przez co
                    # w kazdym LSB mamy zakodowana 1 bit z wiadomosci )
                    pixel[2] = pixel[2] & 0xFE | int(binary_message[index])
                    #set pixel dla obrazu z wiadomoscia
                    encoded_image.putpixel((x, y), tuple(pixel))
                    index += 1

        # Zapis nowego obrazu
        encoded_image_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                          filetypes=[("PNG Files", "*.png"),
                                                                     ("JPEG Files", "*.jpg *.jpeg"),
                                                                     ("TIFF Files", "*.tiff *.tif")])
        encoded_image.save(encoded_image_path)
        print("Image successfully encoded.")

    except FileNotFoundError:
        print("Image file not found.")
    except ValueError as e:
        print("Error:", e)
    except Exception as e:
        print("An error occurred:", e)


def decode_image():
    global encoded_image_path
    try:
        # Otwarcie obrazu
        encoded_image = Image.open(encoded_image_path)

        # Z każdej wartości piksela wyciąga bity i wrzuca do binary_message
        binary_message = ""
        for x in range(encoded_image.width):
            for y in range(encoded_image.height):
                pixel = encoded_image.getpixel((x, y))
                binary_message += str(pixel[2] & 1)

        # Konwersja binarnego systemu na unicode
        secret_message = ""
        char_count = len(binary_message) // 8
        #Dla każdego bajta
        for i in range(char_count):
            #Wartość ostatniego bita
            byte = binary_message[i * 8: (i + 1) * 8]
            #Konwersja bajta z binarnego
            char = chr(int(byte, 2))
            secret_message += char

        return secret_message

    except FileNotFoundError:
        print("Encoded image file not found.")
    except Exception as e:
        print("An error occurred:", e)


#Przegladaj do zakodowania
def browse_image():
    global image_path
    # Prompt user to select an image file
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.tiff *.tif")])
    image_label.config(text="Selected image: " + image_path)

#Przegladaj do odkodowania
def browse_encoded_image():
    global encoded_image_path
    # Prompt user to select an encoded image file
    encoded_image_path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png"),
                                                               ("JPEG Files", "*.jpg *.jpeg"),
                                                               ("TIFF Files", "*.tiff *.tif")])
    encoded_image_label.config(text="Selected encoded image: " + encoded_image_path)


def decode_button_click():
    secret_message = decode_image()
    if secret_message:
        print("Decoded message:", secret_message)
    else:
        print("Unable to decode the image.")


# Proste gui dla obsługi
window = Tk()
window.title("Steganography Task")
window.geometry("400x400")

browse_button = Button(window, text="Browse Image", command=browse_image)
browse_button.pack()

image_label = Label(window, text="Selected image: ")
image_label.pack()

message_entry = Entry(window)
message_entry.pack()

encode_button = Button(window, text="Encode image", command=encode_image)
encode_button.pack()

space = Label(window, text="--------------------------------------")
space.pack()

browse_encoded_button = Button(window, text="Browse Encoded Image", command=browse_encoded_image)
browse_encoded_button.pack()

encoded_image_label = Label(window, text="Selected encoded image: ")
encoded_image_label.pack()

decode_button = Button(window, text="Decode image", command=decode_button_click)
decode_button.pack()

window.mainloop()
