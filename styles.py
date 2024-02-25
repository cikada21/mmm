from PyQt5.QtGui import QImage, QPainter, QBrush, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider


def set_btn_play_style(button, btn_height, btn_width, btn_play_x, btn_play_y):
    button.setFixedSize(btn_height, btn_width)
    button.move(btn_play_y, btn_play_x)
    button.setStyleSheet("""
        QPushButton {
            background-color: #03262e;
            color: white;
            border-top-left-radius: 10px; border-top-right-radius: 10px;
            font-size: 20px;        /* Увеличиваем размер шрифта */
            padding: 5px;           /* Добавляем отступы */
            width: 20px;
        }
        QPushButton:hover {
            background-color: #042a33;  /* Изменяем цвет при наведении */
        }
        QPushButton:pressed {
            background-color: #032e38;  /* Изменяем цвет при нажатии */
        }
    """)


def set_btn_switch_style(button, btn_height, btn_width, btn_play_y, btn_play_x):
    button.setFixedSize(btn_height, btn_width)
    button.move(btn_play_y, btn_play_x)
    button.setStyleSheet("""
            QPushButton {
                background-color: #03262e;
                color: white;
                border-top-left-radius: 10px; border-top-right-radius: 10px;
                font-size: 20px;        /* Увеличиваем размер шрифта */
                padding: 5px;           /* Добавляем отступы */
                width: 20px;
            }
            QPushButton:hover {
                background-color: #042a33;  /* Изменяем цвет при наведении */
            }
            QPushButton:pressed {
                background-color: #032e38;  /* Изменяем цвет при нажатии */
            }
        """)


def round_image(img_path, radius):
    # Загрузка изображения
    img = QImage(img_path)

    # Создание выходного изображения с прозрачностью
    out_img = QImage(img.size(), QImage.Format_ARGB32)
    out_img.fill(Qt.transparent)

    # Создание QPainter для рисования на выходном изображении
    painter = QPainter(out_img)
    painter.setRenderHint(QPainter.Antialiasing, True)
    painter.setBrush(QBrush(img))
    painter.setPen(Qt.NoPen)

    # Рисование закругленного прямоугольника
    painter.drawRoundedRect(img.rect(), radius, radius)

    painter.end()

    return QPixmap.fromImage(out_img)


def set_slider_style(slider, btn_height, btn_width, btn_play_x, btn_play_y):
    slider.move(btn_play_x, btn_play_y)
    slider.setFixedSize(200, 20)
    slider.setStyleSheet("""
        QSlider::groove:horizontal {
            height: 8px;
            background: #03151a;
        }
        QSlider::handle:horizontal {
            background: #03242b;
            width: 20px;
            margin: -6px 0;
            border-radius: 10px;
        }
        QSlider::handle:horizontal:hover {
            background: #042a33;
        }
        QSlider::handle:horizontal:pressed {
            background: #032e38;
        }
    """)
