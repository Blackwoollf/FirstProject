import cv2
import numpy as np
import mage as im

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

    # Нахождение диапозона цвета
    lower_range = np.array([36,25,25], dtype=np.uint8)
    upper_range = np.array([86,255,255], dtype=np.uint8)
    mask = cv2.inRange(frame_hsv, lower_range, upper_range)

    # Фильтр для очистки изображения
    poisk = im.Erode(mask)

    # Нахождение радиуса Зеленого цвета
    __, thresh = cv2.threshold(poisk, 127, 255, 0)
    contours_area = []
    front = cv2.FONT_HERSHEY_DUPLEX

    # Поиск контуров нашего диапозона
    contours, hierarchy = cv2.findContours(thresh, 1, 2)

    count_contours = 0

    for c in contours:
        # Пперебираем все найденные контуры в цикле
        x, y, w, h = cv2.boundingRect(c)

        # Вписыват в наш диапозон замкнутый контур прямоугольника
        rect = cv2.minAreaRect(c)
        box1 = cv2.boxPoints(rect)
        # округление координат
        box = np.int0(box1)

        # Находим площадь контура
        area2 = cv2.contourArea(c)
        if 200 < area2 < 20000:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Наименует объекты на захваченном изображении
            cv2.putText(frame, str(round(area2)), (x, y), front, 1.0, (0, 255, 0), lineType=cv2.LINE_AA)
            print(area2)
            count_contours += 1
         # вычисляем площадь и отсекаем контуры с маленькой площадью
            area = int(rect[1][0] * rect[1][1])
            if area > 500:
         # По координаты нашего диапозона накладываем контур
                cv2.drawContours(frame, [box], 0, (0, 255, 255), 2)
    # Счетчик, на выводе экрана подсчитывает объекты
    str_count = "Count: {}".format(count_contours)
    # Наименует объекты на захваченном изображении
    cv2.putText(frame, str_count, (10, 25), front, 0.5, (0, 255, 0), lineType=cv2.LINE_AA)

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