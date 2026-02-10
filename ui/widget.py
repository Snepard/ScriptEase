from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QApplication
)
from PyQt5.QtCore import (
    QThread, pyqtSignal, Qt, QPoint, QRectF
)
from PyQt5.QtGui import (
    QFont, QPainter, QPainterPath, QPixmap
)
import os

from core.promptEngine import PromptEngine
from core.llmEngine import get_llm


# BACKGROUND WORKER

class LLMWorker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, llm, prompt):
        super().__init__()
        self.llm = llm
        self.prompt = prompt

    def run(self):
        result = self.llm.generate(self.prompt)
        self.finished.emit(result)


# MAIN WIDGET

class ScriptEaseWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("ScriptEaseRoot")
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(520, 560)
        self.setStyleSheet(self._main_style())

        self.llm = get_llm()
        self.prompt_engine = PromptEngine()
        self.worker = None
        self._drag_pos = QPoint()
        self._internal_clipboard_change = False
        self._build_ui()
        self._setup_clipboard_listener()

    def _setup_clipboard_listener(self):
        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self._on_clipboard_change)

    def _on_clipboard_change(self):
        if self._internal_clipboard_change:
            return

        text = self.clipboard.text().strip()
        if text:
            self.input_box.setPlainText(text)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRectF(self.rect()).adjusted(1, 1, -1, -1)
        path = QPainterPath()
        path.addRoundedRect(rect, 22, 22)

        painter.fillPath(path, self.palette().window())

    # UI

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(12)

        # Top-right window buttons
        header = QHBoxLayout()
        header.addStretch()

        self.min_btn = QPushButton("–")
        self.close_btn = QPushButton("✕")

        for btn in (self.min_btn, self.close_btn):
            btn.setFixedSize(30, 30)
            btn.setStyleSheet(self._header_btn())
            btn.setCursor(Qt.PointingHandCursor)

        self.close_btn.setStyleSheet(self._header_btn(close=True))

        self.min_btn.clicked.connect(self.showMinimized)
        self.close_btn.clicked.connect(self.close)

        header.addWidget(self.min_btn)
        header.addWidget(self.close_btn)
        layout.addLayout(header)

        # Robo (left) + title (right), bottom touching input box
        robo_input_layout = QVBoxLayout()
        robo_input_layout.setSpacing(0)
        robo_input_layout.setContentsMargins(0, 0, 0, 0)

        robo_title_row = QHBoxLayout()
        robo_title_row.setContentsMargins(0, 0, 0, 0)

        robo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "robo.png")
        robo_pixmap = QPixmap(robo_path)
        if not robo_pixmap.isNull():
            robo_pixmap = robo_pixmap.scaledToHeight(80, Qt.SmoothTransformation)
        self.robo_label = QLabel()
        self.robo_label.setPixmap(robo_pixmap)
        self.robo_label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.robo_label.setStyleSheet("border:none; background:transparent;")
        self.robo_label.setContentsMargins(0, 0, 0, 0)
        robo_title_row.addWidget(self.robo_label)

        title = QLabel("ScriptEase")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        title.setStyleSheet("color:#1e293b; border:none; background:transparent;")
        title.setContentsMargins(4, 0, 0, 8)
        robo_title_row.addWidget(title)
        robo_title_row.addStretch()

        robo_input_layout.addLayout(robo_title_row)

        box_font = QFont("Segoe UI", 12)
        BOX_H = 120

        self.input_box = QTextEdit()
        self.input_box.setFont(box_font)
        self.input_box.setFixedHeight(BOX_H)
        self.input_box.setPlaceholderText("Clipboard text will appear here…")
        self.input_box.setStyleSheet(self._textbox_style())
        robo_input_layout.addWidget(self.input_box)

        layout.addLayout(robo_input_layout)

        btn_row = QHBoxLayout()
        btn_font = QFont("Segoe UI", 12, QFont.Bold)

        self.rewrite_btn = QPushButton("Rewrite")
        self.summarize_btn = QPushButton("Summarize")
        self.improve_btn = QPushButton("Improve")

        for btn in (self.rewrite_btn, self.summarize_btn, self.improve_btn):
            btn.setFont(btn_font)
            btn.setFixedHeight(46)
            btn.setCursor(Qt.PointingHandCursor)

        self.rewrite_btn.setStyleSheet(self._blue_btn())
        self.summarize_btn.setStyleSheet(self._orange_btn())
        self.improve_btn.setStyleSheet(self._purple_btn())

        self.rewrite_btn.clicked.connect(lambda: self.run_task("rewrite"))
        self.summarize_btn.clicked.connect(lambda: self.run_task("summarize"))
        self.improve_btn.clicked.connect(lambda: self.run_task("improve"))

        btn_row.addWidget(self.rewrite_btn)
        btn_row.addWidget(self.summarize_btn)
        btn_row.addWidget(self.improve_btn)
        layout.addLayout(btn_row)

        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.setFont(box_font)
        self.output_box.setFixedHeight(BOX_H)
        self.output_box.setPlaceholderText("Output will appear here…")
        self.output_box.setStyleSheet(self._textbox_style())
        layout.addWidget(self.output_box)

        bottom = QHBoxLayout()

        self.copy_btn = QPushButton("Copy Output")
        self.copy_btn.setFont(btn_font)
        self.copy_btn.setFixedHeight(48)
        self.copy_btn.setMinimumWidth(360)
        self.copy_btn.setStyleSheet(self._copy_btn())
        self.copy_btn.setCursor(Qt.PointingHandCursor)
        self.copy_btn.clicked.connect(self.copy_output)

        bottom.addWidget(self.copy_btn)
        layout.addLayout(bottom)

    # TASK

    def run_task(self, task):
        text = self.input_box.toPlainText().strip()
        if not text:
            self.output_box.setText("⚠️ Input is empty.")
            return

        self.output_box.setText("Thinking… ⏳")
        prompt = self.prompt_engine.build(task, text)

        self.worker = LLMWorker(self.llm, prompt)
        self.worker.finished.connect(self.on_result_ready)
        self.worker.start()

    def on_result_ready(self, result):
        self.output_box.setText(result)
        self.worker = None

    def copy_output(self):
        text = self.output_box.toPlainText().strip()
        if text:
            self._internal_clipboard_change = True
            QApplication.clipboard().setText(text)
            self._internal_clipboard_change = False
            self.output_box.append("\n\n✅ Copied to clipboard.")

    def show_and_focus(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._drag_pos = e.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(e.globalPos() - self._drag_pos)

    # STYLES

    def _main_style(self):
        return """
        QWidget#ScriptEaseRoot {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #eef6ff,
                stop:1 #f3ecff
            );
            border-radius: 22px;
            border: 2px solid #c7d2fe;
        }
        """

    def _textbox_style(self):
        return """
        QTextEdit {
            background: white;
            border-radius: 16px;
            padding: 10px;
            border: 2px solid #dbeafe;
        }
        """

    def _header_btn(self, close=False):
        bg = "#ef4444" if close else "#64748b"
        hover = "#dc2626" if close else "#475569"
        return f"""
        QPushButton {{
            background:{bg};
            color:white;
            border-radius:15px;
            font-weight:bold;
        }}
        QPushButton:hover {{
            background:{hover};
        }}
        """

    def _blue_btn(self):
        return "QPushButton{background:#38bdf8;color:white;border-radius:14px;}QPushButton:hover{background:#0ea5e9;}"

    def _orange_btn(self):
        return "QPushButton{background:#fb923c;color:white;border-radius:14px;}QPushButton:hover{background:#f97316;}"

    def _purple_btn(self):
        return "QPushButton{background:#a78bfa;color:white;border-radius:14px;}QPushButton:hover{background:#8b5cf6;}"

    def _copy_btn(self):
        return "QPushButton{background:#22c55e;color:white;border-radius:18px;}QPushButton:hover{background:#16a34a;}"
