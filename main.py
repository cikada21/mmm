import os
import sys

from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QMainWindow, QSlider, QSizePolicy
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QTimer


from styles import *

win_height = 360
win_width = 400
btn_height = 60
btn_width = 40
btn_play_x = int((win_height - btn_height) / 2)
btn_play_y = int((win_width - btn_width) / 2) + 180


def library_check(lst):
    return [(os.listdir(f'library/{s}')[0], os.listdir(f'library/{s}')[1]) for s in lst if s[-2:] == 'v=']


def select_img(num):
    return f'library/{sounds[num][:-3]}v=/{images[num]}'


def select_sound(num):
    return f'library/{sounds[num][:-3]}v=/{sounds[num]}'


library = library_check(os.listdir('library'))
images = [i[0] for i in library]
sounds = [i[1] for i in library]


def edit_active_img(self, edit):
    n = self.selector + edit
    if n == len(images):
        self.selector = 0
    elif n < 0:
        self.selector = len(images)-1
    else:
        self.selector = n
    print(self.selector)
    self.pixmap = round_image(select_img(self.selector), 30)
    self.active_img.setPixmap(
        self.pixmap.scaled(256, 256, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Обновляем изображение
    self.player.setMedia(QMediaContent(QUrl.fromLocalFile(select_sound(self.selector))))
    self.player.play()
    self.btn_play.setText('-')
    self.stata = False
    return self.selector


def set_clock(ms):
    h = int(ms // 360000)
    m = int(ms // 60000 - h * 60)
    s = int(ms // 1000 - (m * 60) - (h * 3600))
    return '{:02}:{:02}'.format(m, s) if not h else '{:02}:{:02}:{:02}'.format(h, m, s)


class Win(QMainWindow):
    def __init__(self):
        super(Win, self).__init__()

        self.timer = QTimer()
        self.timer.timeout.connect(self.pos_track)
        self.timer.start(1000)  # Запускаем таймер каждую секунду

        self.stata = True
        self.selector = 0
        self.track_position = 0
        self.player = QMediaPlayer()
        self.setGeometry(1500, 600, win_height, win_width)
        self.setFixedSize(win_height, win_width)

        self.setWindowTitle("Мое окно")
        self.setStyleSheet(f"""
                    background-color: black;
                    color: white;
                    property-alignment: AlignCenter;
                """)

        self.active_img = QLabel(self)
        self.pixmap = round_image(select_img(self.selector), 30)
        self.active_img.setPixmap(self.pixmap.scaled(256, 256, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.active_img.move(btn_play_x - 256, btn_play_y - 476)
        self.active_img.setAlignment(Qt.AlignCenter)
        self.active_img.setFixedSize(564, 564)

        self.text_track_pos = QLabel(self)
        self.text_track_pos.move(btn_play_x-80, btn_play_y-65)
        self.text_track_pos.setFixedSize(60, 40)
        self.text_track_pos.setText('00:00')

        self.text_track_len = QLabel(self)
        self.text_track_len.move(btn_play_x+80, btn_play_y - 65)
        self.text_track_len.setFixedSize(60, 40)
        self.text_track_len.setText(set_clock(1111))

        self.slider = QSlider(Qt.Horizontal, self)
        set_slider_style(self.slider, 200, 20, btn_play_x-70, btn_play_y-30)

        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(select_sound(self.selector))))

        self.btn_play = QPushButton('+', self)
        set_btn_play_style(self.btn_play, btn_height, btn_width, btn_play_y, btn_play_x)
        self.btn_play.clicked.connect(self.change_btn_play)

        self.btn_back = QPushButton('<', self)
        set_btn_switch_style(self.btn_back, btn_height, btn_width, btn_play_x-80, btn_play_y)
        self.btn_back.clicked.connect(self.change_btn_back)

        self.btn_next = QPushButton('>', self)
        set_btn_switch_style(self.btn_next, btn_height, btn_width, btn_play_x+80, btn_play_y)
        self.btn_next.clicked.connect(self.change_btn_next)

    def change_btn_play(self):
        if self.stata:
            print('-')
            self.player.setPosition(self.track_position)
            self.player.play()
            self.btn_play.setText('-')
            self.stata = False
        else:
            print('+')
            self.track_position = self.player.position()
            self.player.stop()
            self.btn_play.setText('+')
            self.stata = True
        print(self.selector)

    def change_btn_back(self):
        self.selector = edit_active_img(self, 1)

    def change_btn_next(self):
        self.selector = edit_active_img(self, -1)

    def pos_track(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.track_position = self.player.position()  # Получаем текущую позицию трека
        else:
            self.track_position = self.track_position
        print(f"Текущая позиция трека: {self.track_position} мс")
        self.text_track_pos.setText(f'{self.track_position}')



def application():
    app = QApplication(sys.argv)
    window = Win()

    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    application()
