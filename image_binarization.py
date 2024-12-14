from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import cv2
import numpy as np
from tkinter import messagebox
import time

root = Tk()
def openfilename():
    filename = filedialog.askopenfilename(title='Выбор изображения')
    return filename

def program():
    messagebox.showinfo(title="О программе", message="""Наименование: Бинаризация изображений
Автор: Агаджанян Алёна Самвеловна
Дата создания: 2024 год""")


def tutorials():
    messagebox.showinfo(title="О программе", message="""Для получения бинаризированного изображения вам необходимо нажать \"Выбрать изображение\" во вкладке \"Файл\".
Вы увидите на экране бинаризированные изображения, полученные разными методами.
Вы можете сохранить их по отдельности.""")

def save_method_niblack():
    if niblack_imgtk != '':
        files = [('JPEG files', '*.jpeg'),
                 ('PNG Files', '*.png'),
                 ('Python Files', '*.py')]
        cv2.imwrite(filedialog.asksaveasfilename(title=u'save file ', filetypes=files, defaultextension=files), niblack_image)
        messagebox.showinfo(title="Информация", message="Изображение сохранено")
    else:
        messagebox.showerror(title="Ошибка", message="Необходимо выбрать изображение")

def save_method_bernsen():
    if bernsen_imgtk != '':
        files = [('JPEG files', '*.jpeg'),
                 ('PNG Files', '*.png'),
                 ('Python Files', '*.py')]
        cv2.imwrite(filedialog.asksaveasfilename(title=u'save file ', filetypes=files, defaultextension=files), bernsen_imgtk)
        messagebox.showinfo(title="Информация", message="Изображение сохранено")
    else:
        messagebox.showerror(title="Ошибка", message="Необходимо выбрать изображение")

def save_method_christian():
    if christian_imgtk != '':
        files = [('JPEG files', '*.jpeg'),
                 ('PNG Files', '*.png'),
                 ('Python Files', '*.py')]
        cv2.imwrite(filedialog.asksaveasfilename(title=u'save file ', filetypes=files, defaultextension=files), christian_imgtk)
        messagebox.showinfo(title="Информация", message="Изображение сохранено")
    else:
        messagebox.showerror(title="Ошибка", message="Необходимо выбрать изображение")

def niblack_thresholding(image, window_size=15, k=-0.2):
    start_time = time.perf_counter_ns ()
    # Преобразование изображения в градации серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Определяем размеры окна
    half_window = window_size // 2

    # Создаем пустую маску для бинарного изображения
    binary_image = np.zeros_like(gray)

    # Проходим по каждому пикселю изображения
    for i in range(half_window, gray.shape[0] - half_window):
        for j in range(half_window, gray.shape[1] - half_window):
            # Получаем локальное окно
            local_window = gray[i - half_window:i + half_window + 1, j - half_window:j + half_window + 1]
            
            # Вычисляем среднее и стандартное отклонение
            mean = np.mean(local_window)
            std_dev = np.std(local_window)

            # Вычисляем порог по методу Ниблэка
            threshold = mean + k * std_dev

            # Применяем порог к текущему пикселю
            if gray[i, j] > threshold:
                binary_image[i, j] = 255
    
    timecode = time.perf_counter_ns () - start_time
    return binary_image, timecode/1000000000

def bernsen_thresholding(image, window_size=15, delta=10):
    start_time = time.perf_counter_ns ()
    # Преобразование изображения в градации серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Определяем размеры окна
    half_window = window_size // 2

    # Создаем пустую маску для бинарного изображения
    binary_image = np.zeros_like(gray)

    # Проходим по каждому пикселю изображения
    for i in range(half_window, gray.shape[0] - half_window):
        for j in range(half_window, gray.shape[1] - half_window):
            # Получаем локальное окно
            local_window = gray[i - half_window:i + half_window + 1, j - half_window:j + half_window + 1]
            
            # Находим минимальное и максимальное значение в окне
            min_val = float(np.min(local_window))
            max_val = float(np.max(local_window))

            # Вычисляем порог по методу Бернсена
            threshold = (min_val + max_val) / 2

            # Применяем порог с учетом дельты
            if gray[i, j] > threshold + delta:
                binary_image[i, j] = 255
            elif gray[i, j] < threshold - delta:
                binary_image[i, j] = 0
            else:
                binary_image[i, j] = 127  # Полутоны (можно изменить на другой подход)
    timecode = time.perf_counter_ns () - start_time
    return binary_image, timecode/1000000000

def christian_thresholding(image, window_size=15, c=10):
    start_time = time.perf_counter_ns ()
    # Преобразуем изображение в оттенки серого
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Вычисляем среднее значение в окне
    mean = cv2.boxFilter(gray_image, ddepth=-1, ksize=(window_size, window_size))
    
    # Вычисляем порог по формуле Кристиана
    threshold = mean - c
    
    # Бинаризация изображения
    binary_image = (gray_image > threshold).astype(np.uint8) * 255

    timecode = time.perf_counter_ns () - start_time
    return binary_image, timecode/1000000000

def mse(imageA, imageB):
    imageA = np.array(imageA)
    imageB = np.array(imageB)
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

img = ''

def main():
    x = openfilename()
    global img, img_copy
    img = Image.open(x)
    img_np = np.array(img)
    img_copy_gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    img = img.resize((300, 300), Image.Resampling.LANCZOS)
    begin_image = ImageTk.PhotoImage(img)
    global begin_image_pane
    begin_image_pane = Label(root, image=begin_image)
    begin_image_pane.image = begin_image
    begin_image_pane.place(x=30, y=30)

    global label_1
    label_1 = Label(text="Начальное изображение")
    label_1.place(x=100, y=332)

    # niblack
    global niblack_image, niblack_imgtk
    niblack_image, niblack_time = niblack_thresholding(img_np)
    niblack_image_pil = Image.fromarray(niblack_image)

    niblack_image_pil = niblack_image_pil.resize((300, 300), Image.Resampling.LANCZOS)

    niblack_imgtk = ImageTk.PhotoImage(niblack_image_pil)
    global niblack_pane
    niblack_pane = Label(root, image=niblack_imgtk)
    niblack_pane.image = niblack_imgtk
    niblack_pane.place(x=450, y=30)

    global label_2
    label_2 = Label(text="Результат работы метода Ниблэка\nВремя работы метода: " + str(niblack_time) + " секунд\nMSE: " + str(mse(img_copy_gray, niblack_image)))
    label_2.place(x=500, y=332)

    # bernsen
    global bernsen_image, bernsen_imgtk
    bernsen_image, bernsen_time = bernsen_thresholding(img_np)
    bernsen_image_pil = Image.fromarray(bernsen_image)

    bernsen_image_pil = bernsen_image_pil.resize((300, 300), Image.Resampling.LANCZOS)

    bernsen_imgtk = ImageTk.PhotoImage(bernsen_image_pil)
    global bernsen_pane
    bernsen_pane = Label(root, image=bernsen_imgtk)
    bernsen_pane.image = bernsen_imgtk
    bernsen_pane.place(x=30, y=390)

    global label_3
    label_3 = Label(text="Результат работы метода Бернсена\nВремя работы метода: " + str(bernsen_time) + " секунд\nMSE: " + str(mse(img_copy_gray, bernsen_image)))
    label_3.place(x=80, y=695)

    # christian
    global christian_image, christian_imgtk
    christian_image, christian_time = christian_thresholding(img_np)
    christian_image_pil = Image.fromarray(christian_image)

    christian_image_pil = christian_image_pil.resize((300, 300), Image.Resampling.LANCZOS)

    christian_imgtk = ImageTk.PhotoImage(christian_image_pil)
    global christian_pane
    christian_pane = Label(root, image=christian_imgtk)
    christian_pane.image = christian_imgtk
    christian_pane.place(x=450, y=390)

    global label_4
    label_4 = Label(text="Результат работы метода Кристиана\nВремя работы метода: " + str(christian_time) + " секунд\nMSE: " + str(mse(img_copy_gray, christian_image)))
    label_4.place(x=500, y=695)

def delete_image():
    if img!='':
        print(img)
        begin_image_pane.destroy()
        niblack_pane.destroy()
        bernsen_pane.destroy()
        christian_pane.destroy()
        label_1.destroy()
        label_2.destroy()
        label_3.destroy()
        label_4.destroy()
    else:
        messagebox.showerror(title="Ошибка", message="Необходимо выбрать изображение")


root.title("Binary image")
root.geometry("800x750")
root.resizable()
root.resizable(width=True, height=True)
root.option_add("*tearOff", FALSE)

main_menu = Menu()
file_menu = Menu()
settings_menu = Menu()

settings_menu.add_command(label="Метод Ниблэка", command=save_method_niblack)
settings_menu.add_command(label="Метод Бернсена", command=save_method_bernsen)
settings_menu.add_command(label="Метод Кристиана", command=save_method_christian)

file_menu.add_command(label="Выбрать изображение", command=main)
file_menu.add_command(label="Удалить изображение", command=delete_image)
file_menu.add_cascade(label="Сохранить", menu=settings_menu)

main_menu.add_cascade(label="Файл", menu=file_menu)
main_menu.add_command(label="Помощь", command=tutorials)
main_menu.add_command(label="О программе", command=program)
main_menu.add_command(label="Выход", command=root.destroy)

root.config(menu=main_menu)

root.mainloop()