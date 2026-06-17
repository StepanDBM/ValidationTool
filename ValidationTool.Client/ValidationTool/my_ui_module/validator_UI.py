from PySide6 import QtWidgets, QtGui, QtCore
import maya.cmds as cmds

from config.validation_profile import ValidationProfile
from core.runner import run_pipeline


from core.validation_system import FixMode
import config.check_categories as check_categories
from misc_tools.DCC.Maya.maya_adapter import extract_maya_scene
from misc_tools.DCC.Maya.maya_safeMultiTool import _get_scene_path


class Severity:
    ALL = "ALL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


# ===================== COLOR DELEGATE =====================

class ColorDelegate(QtWidgets.QStyledItemDelegate):

    def paint(self, painter, option, index):
        severity = index.model().data(index.sibling(index.row(), 0), QtCore.Qt.DisplayRole)

        if severity == "ERROR":
            option.palette.setColor(QtGui.QPalette.Text, QtGui.QColor(255, 80, 80))
        elif severity == "WARNING":
            option.palette.setColor(QtGui.QPalette.Text, QtGui.QColor(255, 180, 0))
        else:
            option.palette.setColor(QtGui.QPalette.Text, QtGui.QColor(180, 180, 180))

        super().paint(painter, option, index)


# ===================== MAIN WINDOW =====================

class ValidatorWindow(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Validation Tool")
        self.resize(950, 520)

        self.current_filter = Severity.ALL

        self.build_ui()
        self.create_connections()

    # ---------------- UI ----------------

    def build_ui(self):

        self.run_button = QtWidgets.QPushButton("Run Validation")

        self.btn_all = QtWidgets.QPushButton("ALL")
        self.btn_error = QtWidgets.QPushButton("ERROR")
        self.btn_warning = QtWidgets.QPushButton("WARNING")
        self.btn_info = QtWidgets.QPushButton("INFO")

        self.category_combo = QtWidgets.QComboBox()
        self.category_combo.addItem("ALL", "ALL")
        self.category_combo.addItem("Geometry", check_categories.GEOMETRY)
        self.category_combo.addItem("UV", check_categories.UV)
        self.category_combo.addItem("Transform", check_categories.TRANSFORM)
        self.category_combo.addItem("Naming", check_categories.NAMING)

        self.view = QtWidgets.QTreeView()

        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(
            ["Severity", "Asset", "Stage", "Message", "Fix"]
        )

        self.view.setModel(self.model)
        header = self.view.header()
        self.view.setSortingEnabled(True)
        
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)  # Severity
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)           # Asset
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)  # Stage
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)           # Message
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)  # Fix 

        self.view.setRootIsDecorated(False)
        self.view.setAlternatingRowColors(True)
        self.view.setItemDelegate(ColorDelegate())

        # ---------------- FILTER BAR ----------------

        filter_layout = QtWidgets.QHBoxLayout()
        filter_layout.addWidget(self.btn_all)
        filter_layout.addWidget(self.btn_error)
        filter_layout.addWidget(self.btn_warning)
        filter_layout.addWidget(self.btn_info)

        # ---------------- TOP BAR ----------------

        top_bar = QtWidgets.QHBoxLayout()

        label = QtWidgets.QLabel("Category:")
        label.setFixedWidth(70)

        top_bar.addWidget(label)
        top_bar.addWidget(self.category_combo)

        top_bar.addSpacing(20)
        top_bar.addStretch()
        top_bar.addLayout(filter_layout)

        # ---------------- MAIN LAYOUT ----------------

        layout = QtWidgets.QVBoxLayout(self)

        layout.addWidget(self.run_button)
        layout.addLayout(top_bar)
        layout.addWidget(self.view)

    # ---------------- Connections ----------------

    def create_connections(self):

        self.run_button.clicked.connect(self.run_validation)
        self.category_combo.currentIndexChanged.connect(self.run_validation)

        self.btn_all.clicked.connect(lambda: self.apply_filter(Severity.ALL))
        self.btn_error.clicked.connect(lambda: self.apply_filter(Severity.ERROR))
        self.btn_warning.clicked.connect(lambda: self.apply_filter(Severity.WARNING))
        self.btn_info.clicked.connect(lambda: self.apply_filter(Severity.INFO))

        self.view.clicked.connect(self.on_view_clicked)
        self.view.doubleClicked.connect(self.frame_mesh)

    # ---------------- CORE ----------------

    def run_validation(self):
        self.model.removeRows(0, self.model.rowCount())

        scene_setup, objects = extract_maya_scene()
        profile = ValidationProfile(
            enabled_categories={
                self.category_combo.currentData()
            } if self.category_combo.currentData() != "ALL" else set()
        )

        context = {
            "headless": 0,
            "dcc": "Maya",
            "path": _get_scene_path(),
            "scene_setup": scene_setup
        }

        result = run_pipeline(objects, context, profile=profile)

        
        for issue in result.issues:

            severity_item = QtGui.QStandardItem(issue.severity.value)
            asset_item = QtGui.QStandardItem(issue.object_name)
            stage_item = QtGui.QStandardItem(issue.stage)
            message_item = QtGui.QStandardItem(issue.message)

            fix_item = QtGui.QStandardItem("")

            asset_item.setData(issue.object_name, QtCore.Qt.UserRole)
            

            self.model.appendRow([
                severity_item,
                asset_item,
                stage_item,
                message_item,
                fix_item
            ])
            button = None

            if issue.fix_mode == FixMode.SEMI:
                button = QtWidgets.QPushButton("Fix")
                button.clicked.connect(lambda _, i=issue: self.run_fix(i))

            elif issue.fix_mode == FixMode.NONE:
                 fix_item.setText("Manual Fixing")

            if button:
                button.setFixedHeight(22)
                button.setMinimumWidth(80)

                index = self.model.index(row_index, 4)
                self.view.setIndexWidget(index, button)


            row_index = self.model.rowCount() - 1

    # ---------------- FILTERING ----------------

    def apply_filter(self, severity):

        self.current_filter = severity

        for row in range(self.model.rowCount()):

            index = self.model.index(row, 0)
            row_severity = self.model.data(index)

            visible = (
                severity == Severity.ALL or
                row_severity == severity
            )

            self.view.setRowHidden(row, QtCore.QModelIndex(), not visible)

    # ---------------- CLICK HANDLER ----------------

    def on_view_clicked(self, index):

        row = index.row()
        column = index.column()

        if column == 4:

            item = self.model.item(row, 4)
            issue = item.data(QtCore.Qt.UserRole)

            if issue and issue.fix_mode.value == "SEMI":
                self.run_fix(issue)

            return

        asset_index = index.sibling(row, 1)
        asset_name = self.model.data(asset_index, QtCore.Qt.UserRole)

        if asset_name and cmds.objExists(asset_name):
            cmds.select(asset_name)


    def run_fix(self, issue):
        print(f"[FIXING THIS: ] {issue.check_name} → {issue.object_name}")


    def frame_mesh(self, index):

        asset_index = index.sibling(index.row(), 1)
        asset_name = self.model.data(asset_index, QtCore.Qt.UserRole)

        if asset_name and cmds.objExists(asset_name):
            cmds.select(asset_name)
            cmds.viewFit()


class IssueSortProxy(QtCore.QSortFilterProxyModel):

    def lessThan(self, left, right):

        model = self.sourceModel()

        issue_left = model.item(left.row(), 4).data(QtCore.Qt.UserRole)
        issue_right = model.item(right.row(), 4).data(QtCore.Qt.UserRole)

        from core.validation_system import FixMode

        left_priority = 0
        right_priority = 0

        if issue_left and issue_left.fix_mode == FixMode.SEMI:
            left_priority = -1  # button-having rows are _prior_ to char 'a' in alphabetic sorting

        if issue_right and issue_right.fix_mode == FixMode.SEMI:
            right_priority = -1

        if left_priority != right_priority:
            return left_priority < right_priority

        left_data = model.data(left)
        right_data = model.data(right)

        return str(left_data).lower() < str(right_data).lower()