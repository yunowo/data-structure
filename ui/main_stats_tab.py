from itertools import islice
from os import path, getcwd

from PIL import ImageQt
from PyQt5.QtChart import QChart, QChartView, QHorizontalBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtWidgets import QTableWidgetItem
from wordcloud import WordCloud, STOPWORDS


class MainStatsTab:
    def __init__(self, main_window):
        self.w = main_window

        self.d = self.w.inverse_index.count
        self.index_word()
        self.show_line_graph()
        self.word_cloud()
        self.w.cloud_button.clicked.connect(self.word_cloud)

    def index_word(self):
        self.w.word_table.setRowCount(len(self.d))
        self.w.word_table.setColumnCount(2)
        self.w.word_table.setHorizontalHeaderLabels(['字符', '频度'])
        for i, k in enumerate(self.d):
            self.w.word_table.setItem(i, 0, QTableWidgetItem(str(k)))
            self.w.word_table.setItem(i, 1, QTableWidgetItem(str(self.d[k])))
        self.w.word_table.resizeColumnsToContents()

    def show_line_graph(self):
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

        cv = QChartView(c)
        cv.setRenderHint(QPainter.Antialiasing)
        self.w.bar_graph_container.addWidget(cv)

    def word_cloud(self):
        width, height = self.w.word_cloud.width(), self.w.word_cloud.height() - 5
        font = path.join(getcwd(), 'ui', 'src', 'font', 'Quicksand-Regular.ttf')
        wc = WordCloud(width=width, height=height, background_color='white', colormap='jet', font_path=font,
                       max_font_size=100, max_words=500, stopwords=set(STOPWORDS))
        word_cloud = wc.generate_from_frequencies(self.d)
        image = word_cloud.to_image()
        qp = ImageQt.toqpixmap(image)
        self.w.word_cloud.setPixmap(qp)
