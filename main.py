import cv2
import numpy as np
import image as im

# Выбор камеры python open cv уменьшить видео с камеры
cap = cv2.VideoCapture(0)
# VideoCapture создание объекта
cv2.waitKey(0)

while(True):
    # Захват за кадром
    # Получение кадров из камеры
    ret, frame = cap.read()
    # Уменьшаем выводимое изображение на экран
    frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    # Перевод кадра из BGR в HSV
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Нахождение зеленого диапозона цвета
    lower_range = np.array([36,25,25], dtype=np.uint8)
    upper_range = np.array([86,255,255], dtype=np.uint8)
    mask1 = cv2.inRange(frame_hsv, lower_range, upper_range)

    # Нахождение синего диапозона цвета
    mask2 = cv2.inRange(frame_hsv, (110,50,50), (130,255,255))
    # Объеденение двух масок цветов
    mask = cv2.bitwise_or(mask1, mask2)

    # Фильтр для очистки изображения
    poisk = im.Erode(mask)

    # Нахождение радиуса Зеленого цвета
    __, thresh = cv2.threshold(poisk, 127, 255, 0)

    # Задаем переменные
    contours_area = []
    front = cv2.FONT_HERSHEY_DUPLEX

    # Поиск контуров нашего диапозона
    contours, hierarchy = cv2.findContours(thresh, 1, 2)

    count_contours = 0

    for c in contours:
        # Перебираем все найденные контуры в цикле
        x, y, w, h = cv2.boundingRect(c)

        # Вписыват в наш диапозон замкнутый контур прямоугольника
        rect = cv2.minAreaRect(c)
        # Находит четыре вершины повернутого прямоугольника
        box1 = cv2.boxPoints(rect)
        # округление координат
        box = np.int0(box1)

        # Находим площадь внутри контура
        area2 = cv2.contourArea(c)
        if 350 < area2 < 20000:
            # Рисует простой, толстый или заполненный прямоугольник справа вверх.
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Наименует объекты на захваченном изображении
            cv2.putText(frame, str(round(area2)), (x, y), front, 1.0, (0, 255, 0), lineType=cv2.LINE_AA)
            print(area2)
            count_contours += 1
         # вычисляем площадь и отсекаем контуры с маленькой площадью
            area = int(rect[1][0] * rect[1][1])
            if area > 350:
         # По координаты нашего диапозона накладываем контур
                cv2.drawContours(frame, [box], 0, (0, 255, 255), 2)
    # Счетчик, на выводе экрана подсчитывает объекты
    str_count = "Count: {}".format(count_contours)
    # Наименует объекты на захваченном изображении
    cv2.putText(frame, str_count, (10, 25), front, 0.5, (0, 255, 0), lineType=cv2.LINE_AA)

    # Изменение размера изображения
    frame = cv2.resize(frame, (1280, 960))
    cv2.imshow("img2", frame)

    # waitKey отображение кадра в мили седкундах
    key = cv2.waitKey(1)
    if key == ord('q') or key == 27:
        break

    # После получения кадра отпустить его
cap.release()
    # Функция destroyWindow закрывает окно с заданным именем.
cv2.destroyAllWindows()