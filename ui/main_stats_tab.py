from itertools import islice
from os import path, getcwd
from threading import Thread

from PIL import ImageQt
from PyQt5.QtChart import QChart, QChartView, QHorizontalBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtWidgets import QTableWidgetItem
from wordcloud import WordCloud


class MainStatsTab:
    def __init__(self, main_window):
        self.w = main_window

        self.w.num_combo.addItems(['20', '100', '500', '∞'])
        self.w.num_combo.currentIndexChanged.connect(self.num_limit_change)
        self.w.action_filter_toggle.changed.connect(self.filter_change)
        self.w.word_cloud.resizeEvent = self.resize_event

        self.num_limit = 20
        self.filter = True
        self.d = None
        self.cv = None
        self.load()
        self.generating = 0

    def num_limit_change(self, index):
        nums = [20, 100, 500, len(self.d)]
        self.num_limit = nums[index]
        self.index_word(self.num_limit)

    def filter_change(self):
        if self.w.action_filter_toggle.isChecked() == Qt.Unchecked:
            self.filter = False
        else:
            self.filter = True
        self.load()
        self.resize_event(0)

    def load(self):
        if self.filter:
            self.d = self.w.inverse_index.count_filtered
        else:
            self.d = self.w.inverse_index.count
        self.index_word(self.num_limit)
        self.show_bar_chart()

    def index_word(self, num):
        self.w.word_table.clear()
        self.w.word_table.setRowCount(num)
        self.w.word_table.setColumnCount(2)
        self.w.word_table.setHorizontalHeaderLabels(['字符', '频度'])
        for i, k in enumerate(self.d):
            self.w.word_table.setItem(i, 0, QTableWidgetItem(str(k)))
            self.w.word_table.setItem(i, 1, QTableWidgetItem(str(self.d[k])))
        self.w.word_table.resizeColumnsToContents()

    def show_bar_chart(self):
        t20 = list(reversed(list(islice(self.d.items(), 20))))
        bs = QBarSet("")
        bs.append([c[1] for c in t20])
        hbs = QHorizontalBarSeries()
        hbs.append(bs)
        hbs.setBarWidth(0.6)
        hbs.setLabelsVisible(True)
        hbs.setLabelsPosition(QHorizontalBarSeries.LabelsInsideEnd)

        font = QFont()
        font.setFamily('Segoe UI')
        font.setPixelSize(10)
        x = QValueAxis()
        y = QBarCategoryAxis()
        y.append([c[0] for c in t20])
        x.setGridLineVisible(False)
        y.setGridLineVisible(False)
        x.setLabelsFont(font)
        y.setLabelsFont(font)

        c = QChart()
        c.addSeries(hbs)
        c.setAxisY(y, hbs)
        c.setAxisX(x, hbs)
        x.applyNiceNumbers()
        c.setAnimationOptions(QChart.SeriesAnimations)
        c.setBackgroundRoundness(0)
        c.legend().hide()
        c.layout().setContentsMargins(0, 0, 0, 0)

        if self.cv is not None:
            self.w.bar_chart_container.removeWidget(self.cv)
        self.cv = QChartView(c)
        self.cv.setRenderHint(QPainter.Antialiasing)
        self.w.bar_chart_container.addWidget(self.cv)

    def resize_event(self, size):
        if self.generating >= 2:
            return
        self.generating += 1
        if self.generating == 1:
            Thread(target=self.word_cloud).start()

    def word_cloud(self):
        width, height = self.w.word_cloud.width(), self.w.word_cloud.height() - 5
        font = path.join(getcwd(), 'ui', 'src', 'font', 'Quicksand-Regular.ttf')
        wc = WordCloud(width=width, height=height, background_color='white', colormap='jet', font_path=font,
                       max_font_size=100, max_words=500)
        word_cloud = wc.generate_from_frequencies(self.d)
        image = word_cloud.to_image()
        qp = ImageQt.toqpixmap(image)
        self.w.word_cloud.setPixmap(qp)
        self.generating -= 1
        if self.generating > 0:
            self.word_cloud()
