from PySide6 import QtWidgets, QtGui, QtCore
import maya.cmds as cmds

from config.validation_profile import ValidationProfile
from misc_tools.maya_adapter import extract_meshes_from_scene
from core.runner import run_pipeline
from config.validation_config import ValidationConfig
import  config.check_categories as check_categories


class Severity:
    ALL = "ALL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


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


class ValidatorWindow(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Validation Tool")
        self.resize(900, 500)

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
        self.model.setHorizontalHeaderLabels(["Severity", "Asset", "Stage", "Message"])

        self.view.setModel(self.model)
        self.view.setRootIsDecorated(False)
        self.view.setAlternatingRowColors(True)
        self.view.setItemDelegate(ColorDelegate())

        # ---------------- FILTER BAR ----------------

        filter_layout = QtWidgets.QHBoxLayout()
        filter_layout.addWidget(self.btn_all)
        filter_layout.addWidget(self.btn_error)
        filter_layout.addWidget(self.btn_warning)
        filter_layout.addWidget(self.btn_info)

        # ---------------- TOP BAR (CLEANER LAYOUT) ----------------

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

        self.view.clicked.connect(self.select_mesh)
        self.view.doubleClicked.connect(self.frame_mesh)

    # ---------------- Core ----------------

    def run_validation(self):
        self.model.removeRows(0, self.model.rowCount())

        meshes = extract_meshes_from_scene()

        config = ValidationConfig(
            strict_mode=True,
            fail_on_first_error=False,
            auto_fix_enabled=False
        )
        
        profile = ValidationProfile(
            enabled_categories={
                self.category_combo.currentData()
            } if self.category_combo.currentData() != "ALL" else set()
        )
        
        result = run_pipeline(meshes, config, profile=profile)

        for asset in result.assets:
            for stage in asset.stages:
                for issue in stage.issues:

                    severity_item = QtGui.QStandardItem(issue.severity.value)
                    asset_item = QtGui.QStandardItem(issue.asset_name)
                    stage_item = QtGui.QStandardItem(stage.stage)
                    message_item = QtGui.QStandardItem(issue.message)

                    asset_item.setData(issue.asset_name, QtCore.Qt.UserRole)

                    self.model.appendRow([severity_item,
                                          asset_item,
                                          stage_item,
                                          message_item])

    # ---------------- Filtering ----------------

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

    # ---------------- Maya Actions ----------------

    def select_mesh(self, index):

        asset_index = index.sibling(index.row(), 1)
        asset_name = self.model.data(asset_index, QtCore.Qt.UserRole)

        if asset_name:
            cmds.select(asset_name)

    def frame_mesh(self, index):

        asset_index = index.sibling(index.row(), 1)
        asset_name = self.model.data(asset_index, QtCore.Qt.UserRole)

        if asset_name:
            cmds.select(asset_name)
            cmds.viewFit()