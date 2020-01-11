from PySide2 import QtCore
from PySide2.QtCore import Qt, QAbstractItemModel, QModelIndex, QSize
from PySide2.QtGui import QPalette, QFontMetricsF
from PySide2.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget, QTableView, QItemDelegate, QStyle, QHeaderView, QAbstractItemView

import binaryninja
import binaryninjaui
from binaryninja import BinaryView
from binaryninjaui import DockContextHandler, UIActionHandler, LinearView, ViewFrame

from . import widget
from .. import binjaplug, ProcessView

class DebugMemoryWidget(QWidget, DockContextHandler):
	def __init__(self, parent, name, data):
		assert type(data) == binaryninja.binaryview.BinaryView
		self.bv = data
		self.memory_view = ProcessView.DebugProcessView(data)

		QWidget.__init__(self, parent)
		DockContextHandler.__init__(self, self, name)

		self.editor = LinearView(self.memory_view, ViewFrame.viewFrameForWidget(self))
		self.actionHandler = UIActionHandler()
		self.actionHandler.setupActionHandler(self)

		layout = QVBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(0)
		layout.addWidget(self.editor)
		self.setLayout(layout)

	def notifyOffsetChanged(self, offset):
		pass

	def notifyMemoryChanged(self):
		adapter = binjaplug.get_state(self.bv).adapter
		self.memory_view.mark_dirty()
		# Refresh the editor
		self.editor.navigate(adapter.reg_read('rbp'))

	def shouldBeVisible(self, view_frame):
		if view_frame is None:
			return False
		else:
			return True

