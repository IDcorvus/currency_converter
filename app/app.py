from PySide6 import QtWidgets
from currency_converter import CurrencyConverter, RateNotFoundError


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.c = CurrencyConverter()
        self.setWindowTitle("Convertisseur de devises")
        self.setup_ui()
        self.default_values()
        self.setup_connections()


    def setup_ui(self):
        self.layout = QtWidgets.QHBoxLayout(self) # type: ignore
        self.cbb_devisesFrom = QtWidgets.QComboBox()
        self.spn_montant = QtWidgets.QSpinBox()
        self.cbb_devisesTo = QtWidgets.QComboBox()
        self.spn_montantConverti = QtWidgets.QSpinBox()
        self.btn_inverser = QtWidgets.QPushButton()
        self.btn_inverser.setText("Inverser")

        self.layout.addWidget(self.cbb_devisesFrom)
        self.layout.addWidget(self.spn_montant)
        self.layout.addWidget(self.cbb_devisesTo)
        self.layout.addWidget(self.spn_montantConverti)
        self.layout.addWidget(self.btn_inverser)

    def default_values(self):
        self.cbb_devisesFrom.addItems(sorted(list(self.c.currencies))) # type: ignore
        self.cbb_devisesTo.addItems(sorted(list(self.c.currencies))) # type: ignore

        self.spn_montant.setRange(1, 1000000)
        self.spn_montantConverti.setRange(1, 1000000)
        self.spn_montant.setValue(100)
        self.spn_montantConverti.setValue(100)

    def setup_connections(self):
        self.cbb_devisesFrom.activated.connect(self.compute)
        self.cbb_devisesTo.activated.connect(self.compute)
        self.spn_montant.valueChanged.connect(self.compute)
        self.btn_inverser.clicked.connect(self.inverser_devise)

    def compute(self):
        montant = self.spn_montant.value()
        devise_from = self.cbb_devisesFrom.currentText()
        devise_to = self.cbb_devisesTo.currentText()

        try:
            result = self.c.convert(montant, devise_from, devise_to)
        except RateNotFoundError:
            print("Conversion échouée, taux de change introuvable.")
        else:
            self.spn_montantConverti.setValue(result) # type: ignore

    def inverser_devise(self):
        """
        Reverse devises
        """
        devise_from = self.cbb_devisesTo.currentText()
        devise_to = self.cbb_devisesFrom.currentText()
        self.cbb_devisesFrom.setCurrentText(devise_from)
        self.cbb_devisesTo.setCurrentText(devise_to)
        self.compute()

app = QtWidgets.QApplication([])
win = App()
win.show()
app.exec_()