from os import path, getcwd

from PyQt5.QtCore import QSortFilterProxyModel, Qt, QDir
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileSystemModel, QHeaderView


def setup_file_view(view, encoded):
    d = path.join(getcwd(), 'docs')
    model = QFileSystemModel(view)
    model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.AllEntries)
    model.setRootPath(d)
    filtered_model = SortFilter(encoded)
    filtered_model.setSourceModel(model)
    view.setModel(filtered_model)
    view.setRootIndex(filtered_model.mapFromSource(model.index(d)))
    view.setColumnHidden(2, True)
    view.sortByColumn(0, Qt.AscendingOrder)
    for i in range(0, 3):
        view.header().setSectionResizeMode(i, QHeaderView.ResizeToContents)
    return model, filtered_model


class SortFilter(QSortFilterProxyModel):
    def __init__(self, encoded):
        self.encoded = encoded
        super().__init__()

    def headerData(self, section, orientation, role=None):
        if role == Qt.DisplayRole:
            if section == 0:
                return '名称'
            if section == 1:
                return '大小'
            if section == 2:
                return '类型'
            if section == 3:
                return '修改日期'
        return super(SortFilter, self).headerData(section, orientation, role)

    def data(self, index, role=None):
        if role == Qt.DecorationRole and index.column() == 0:
            return QIcon(f":/icon/img/file_{3 if self.encoded else 1}.png")
        return super(SortFilter, self).data(index, role)

    def filterAcceptsRow(self, row, parent):
        if self.filterKeyColumn() == 0:
            index = self.sourceModel().index(row, 0, parent)
            data = self.sourceModel().data(index)
            if parent.data() != 'docs':
                return True
            return not data.startswith('.') and ('encoded' in data) == self.encoded
        return super(SortFilter, self).filterAcceptsRow(row, parent)

    def lessThan(self, index1, index2):
        def name_to_int(i):
            return int(self.sourceModel().data(i).split('_')[0])

        def size_to_int(i):
            a = self.sourceModel().data(i).replace(',', '')
            b = 0
            if 'MB' in a:
                b = int(a.split()[0]) * 1024 * 1024
            if 'KB' in a:
                b = int(a.split()[0]) * 1024
            if 'bytes' in a:
                b = int(a.split()[0])
            return b

        if index1.column() == 0:
            return name_to_int(index1) < name_to_int(index2)
        if index1.column() == 1:
            return size_to_int(index1) < size_to_int(index2)
        return super(SortFilter, self).lessThan(index1, index2)
