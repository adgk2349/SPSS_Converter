import os
import sys
import webbrowser

# ── Qt6 platform plugin 경로 자동 설정 (conda 환경에서 Qt5/Qt6 충돌 방지) ──
def _fix_qt_plugin_path():
    try:
        import PyQt6
        pyqt6_dir = os.path.dirname(PyQt6.__file__)
        plugin_path = os.path.join(pyqt6_dir, "Qt6", "plugins", "platforms")
        if os.path.isdir(plugin_path):
            os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path
    except Exception:
        pass

_fix_qt_plugin_path()

import pandas as pd

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QFileDialog, QMessageBox, QVBoxLayout, QHBoxLayout,
    QFrame, QDialog, QSizePolicy
)
from PyQt6.QtCore import Qt, QPoint, QMimeData, QUrl, QSize
from PyQt6.QtGui import (
    QPainter, QPainterPath, QColor, QBrush, QPen,
    QFont, QFontDatabase, QCursor, QLinearGradient
)

APP_VERSION = "v2.0.0"
GITHUB_URL = "https://github.com/adgk2349/SPSS_Converter"

# ── 색상 팔레트 ───────────────────────────────────────────────
BG_MAIN      = QColor("#1A1A1A")
BG_DROPZONE  = QColor("#111111")
BG_BUTTON    = QColor("#0A84FF")
BG_BTN_HOVER = QColor("#0066CC")
BG_ICON_BTN  = QColor("#2A2A2A")
BG_ICON_HOV  = QColor("#3A3A3A")
BORDER       = QColor("#2A2A2A")
TEXT_WHITE   = "#FFFFFF"
TEXT_GRAY    = "#666666"
TEXT_SGRAY   = "#999999"
RADIUS       = 20          # 창 전체 모서리 반경
DROP_RADIUS  = 14          # 드롭존 모서리 반경


# ══════════════════════════════════════════════════════════════
#  BaseRoundedWidget  —  둥근 모서리 + 완전 투명 배경 기반 클래스
# ══════════════════════════════════════════════════════════════
class BaseRoundedWidget(QWidget):
    """Qt 투명 창 위에 둥근 직사각형을 직접 그려주는 기반 위젯."""

    def __init__(self, parent=None, radius=RADIUS, bg=BG_MAIN, border=BORDER):
        super().__init__(parent)
        self._radius = radius
        self._bg = bg
        self._border = border
        # 윈도우 플래그: 프레임리스 + 투명 배경
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(),
                            self._radius, self._radius)
        painter.setClipPath(path)

        # 배경 채우기
        painter.fillPath(path, QBrush(self._bg))

        # 테두리
        painter.setPen(QPen(self._border, 1))
        painter.drawPath(path)


# ══════════════════════════════════════════════════════════════
#  DropZone  —  파일 드래그 앤 드롭 영역
# ══════════════════════════════════════════════════════════════
class DropZone(QWidget):
    def __init__(self, parent=None, on_drop=None):
        super().__init__(parent)
        self._on_drop = on_drop
        self._hovered = False
        self.setAcceptDrops(True)
        self.setMinimumHeight(220)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)

        # 텍스트는 QLabel로 — QPainter drawText 사용 시 단어 간격 왜곡 문제 있음
        self._label = QLabel("파일을 이곳으로 끌어다 넣으세요\nDrag and drop files here", self)
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label.setStyleSheet(
            f"color: {TEXT_GRAY}; font-size: 14px; background: transparent;"
        )

        layout = QVBoxLayout(self)
        layout.addWidget(self._label)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        bg = QColor("#161616") if self._hovered else BG_DROPZONE
        border = QColor("#0A84FF") if self._hovered else BORDER

        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(),
                            DROP_RADIUS, DROP_RADIUS)

        painter.fillPath(path, QBrush(bg))
        pen = QPen(border, 1.5 if self._hovered else 1,
                   Qt.PenStyle.DashLine if self._hovered else Qt.PenStyle.SolidLine)
        painter.setPen(pen)
        painter.drawPath(path)

    # ── Drag & Drop 이벤트 ──
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            self._hovered = True
            self.update()
            event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        self._hovered = False
        self.update()

    def dropEvent(self, event):
        self._hovered = False
        self.update()
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            if self._on_drop:
                self._on_drop(path)


# ══════════════════════════════════════════════════════════════
#  StyledButton  —  커스텀 둥근 버튼
# ══════════════════════════════════════════════════════════════
class StyledButton(QPushButton):
    def __init__(self, text, parent=None,
                 fg=BG_BUTTON, hover=None,
                 text_color=TEXT_WHITE, radius=21, height=42):
        super().__init__(text, parent)
        self._fg    = fg
        self._hover = hover or fg.lighter(130)
        self._tc    = text_color
        self._r     = radius
        self._base_h = height
        self.setFixedHeight(height)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._hovered = False

    def enterEvent(self, event):
        self._hovered = True
        self.update()

    def leaveEvent(self, event):
        self._hovered = False
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        color = self._hover if self._hovered else self._fg
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), self._r, self._r)
        painter.fillPath(path, QBrush(color))

        painter.setPen(QColor(self._tc))
        f = QFont("", 13, QFont.Weight.Bold)
        painter.setFont(f)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())


# ══════════════════════════════════════════════════════════════
#  AboutDialog  —  Info 팝업
# ══════════════════════════════════════════════════════════════
class AboutDialog(BaseRoundedWidget):
    def __init__(self, parent=None):
        super().__init__(parent, radius=18, bg=BG_MAIN, border=BORDER)
        self.setFixedSize(380, 280)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self._drag_pos = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(8)

        title = QLabel("SPSS Converter")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {TEXT_WHITE}; font-size: 20px; font-weight: bold; background: transparent;")

        ver = QLabel(APP_VERSION)
        ver.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ver.setStyleSheet(f"color: {TEXT_GRAY}; font-size: 12px; background: transparent;")

        desc = QLabel("SPSS to CSV conversion tool.\nBuilt with PyQt6.")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet(f"color: #BBBBBB; font-size: 13px; background: transparent;")

        link = QLabel(f'<a href="{GITHUB_URL}" style="color:#0A84FF;">github.com/adgk2349/SPSS_Converter</a>')
        link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        link.setOpenExternalLinks(True)
        link.setStyleSheet("background: transparent;")

        close_btn = StyledButton("Close", fg=BG_ICON_BTN, hover=BG_ICON_HOV,
                                 radius=15, height=36)
        close_btn.setFixedWidth(100)
        close_btn.clicked.connect(self.close)

        btn_wrap = QHBoxLayout()
        btn_wrap.addStretch()
        btn_wrap.addWidget(close_btn)
        btn_wrap.addStretch()

        layout.addWidget(title)
        layout.addWidget(ver)
        layout.addSpacing(12)
        layout.addWidget(desc)
        layout.addSpacing(8)
        layout.addWidget(link)
        layout.addStretch()
        layout.addLayout(btn_wrap)

    # About 창도 드래그 가능
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)


# ══════════════════════════════════════════════════════════════
#  SPSSConverterApp  —  메인 창
# ══════════════════════════════════════════════════════════════
class SPSSConverterApp(BaseRoundedWidget):
    def __init__(self):
        super().__init__(radius=RADIUS, bg=BG_MAIN, border=BORDER)
        self.setFixedSize(520, 540)
        self.setWindowTitle("SPSS Converter")
        self._drag_pos = None

        self._build_ui()

    # ── UI 구성 ───────────────────────────────────────────────
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 28, 28, 24)
        root.setSpacing(0)

        # ── 헤더 ──
        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)

        title = QLabel("SPSS Converter")
        title.setStyleSheet(
            f"color: {TEXT_WHITE}; font-size: 24px; font-weight: bold; background: transparent;"
        )

        ver_label = QLabel(APP_VERSION)
        ver_label.setStyleSheet(
            f"color: {TEXT_GRAY}; font-size: 12px; background: transparent;"
        )
        ver_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
        ver_label.setContentsMargins(8, 0, 0, 3)

        self.exit_btn = StyledButton("✕", fg=BG_ICON_BTN, hover=QColor("#CC3333"),
                                     radius=14, height=28)
        self.exit_btn.setFixedSize(28, 28)
        self.exit_btn.clicked.connect(self.close)

        header.addWidget(title)
        header.addWidget(ver_label)
        header.addStretch()
        header.addWidget(self.exit_btn)

        root.addLayout(header)
        root.addSpacing(18)

        # ── 드롭존 ──
        self.drop_zone = DropZone(on_drop=self.process_conversion)
        root.addWidget(self.drop_zone)
        root.addSpacing(22)

        # ── 하단 버튼 ──
        footer = QHBoxLayout()
        footer.setSpacing(10)

        self.select_btn = StyledButton(
            "직접 선택 (Select File)",
            fg=BG_BUTTON, hover=BG_BTN_HOVER,
            radius=21, height=44
        )
        self.select_btn.setSizePolicy(QSizePolicy.Policy.Expanding,
                                      QSizePolicy.Policy.Fixed)
        self.select_btn.clicked.connect(self.browse_file)

        self.info_btn = StyledButton(
            "Info", fg=BG_ICON_BTN, hover=BG_ICON_HOV,
            radius=21, height=44
        )
        self.info_btn.setFixedWidth(70)
        self.info_btn.clicked.connect(self.show_about)

        footer.addWidget(self.select_btn)
        footer.addWidget(self.info_btn)
        root.addLayout(footer)
        root.addSpacing(14)

        # ── 상태 레이블 ──
        self.status_label = QLabel("Ready for conversion")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(
            f"color: {TEXT_GRAY}; font-size: 12px; background: transparent;"
        )
        root.addWidget(self.status_label)

    # ── 창 드래그 ─────────────────────────────────────────────
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None

    # ── 파일 처리 ─────────────────────────────────────────────
    def browse_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select SPSS File", "",
            "SPSS Files (*.sav);;All Files (*)"
        )
        if path:
            self.process_conversion(path)

    def process_conversion(self, file_path: str):
        base, ext = os.path.splitext(file_path)
        if ext.lower() != ".sav":
            self._set_status("Invalid file format", "#FF453A")
            QMessageBox.critical(self, "Error", "Please select a valid .sav file.")
            return

        self._set_status("Converting…", "#FF9F0A")
        QApplication.processEvents()

        try:
            df = pd.read_spss(file_path)
            csv_path = f"{base}.csv"
            df.to_csv(csv_path, index=False)
            name = os.path.basename(csv_path)
            self._set_status(f"Done: {name}", "#32D74B")
        except Exception as e:
            self._set_status("Error occurred", "#FF453A")
            QMessageBox.critical(self, "Error",
                                 f"Failed to convert:\n{e}")

    def _set_status(self, text: str, color: str):
        self.status_label.setText(text)
        self.status_label.setStyleSheet(
            f"color: {color}; font-size: 12px; background: transparent;"
        )

    # ── About 팝업 ────────────────────────────────────────────
    def show_about(self):
        dlg = AboutDialog(self)
        # 메인 창 중앙에 배치
        center = self.geometry().center()
        dlg.move(center.x() - dlg.width() // 2,
                 center.y() - dlg.height() // 2)
        dlg.show()


# ══════════════════════════════════════════════════════════════
#  Entry Point
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # High-DPI: QApplication 생성 전에 설정
    os.environ["QT_SCALE_FACTOR_ROUNDING_POLICY"] = "PassThrough"

    app = QApplication(sys.argv)
    app.setApplicationName("SPSS Converter")

    # 시스템 폰트 폴백 (Inter 미설치 환경 대응)
    preferred = [".AppleSystemUIFont", "SF Pro Display",
                 "Helvetica Neue", "Arial", "sans-serif"]
    SYSTEM_FONT = next((f for f in preferred if f in QFontDatabase.families()), "Arial")
    app.setFont(QFont(SYSTEM_FONT, 13))

    window = SPSSConverterApp()
    window.show()
    sys.exit(app.exec())
