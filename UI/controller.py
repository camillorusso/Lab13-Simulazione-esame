import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self.currentYear = None
        self.anni = []
        self.classifica = []
        self.conteggio = 0



    def fillDD_year(self):
        self.anni = self._model.getAllAnni()
        for element in self.anni:
            self._view._ddAnno.options.append(ft.dropdown.Option(text=element,
                                                                 data=element,
                                                                 on_click=self.read_DD_year))

    def read_DD_year(self, e):
        print("read_DD_year called ")
        if e.control.data is None:
            self.currentYear = None
        else:
            self.currentYear = e.control.data
        print(self.currentYear)

    def handleCreaGrafo(self,e):
        y = self.currentYear
        if y is None or y == "":
            self._view.txt_result.controls.append(ft.Text("Selezionare un valore valido per l'anno!"))
            self._view.update_page()
            return
        self._model.buildGraph(y)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {self._model.getNumNodes()} nodi."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {self._model.getNumEdges()} archi."))
        self._view.txt_result.controls.append(ft.Text("Di seguito la classifica completa:"))
        self.classifica = self._model.getAllFinal()
        self.conteggio = 0
        for element, i  in self.classifica:
            self.conteggio += 1
            self._view.txt_result.controls.append(ft.Text(f"{self.conteggio}) {element.forename} {element.surname} con punteggio {i}"))
        self.conteggio = 0
        self._view.update_page()

    def handleCerca(self, e):
        k = self._view._txtIntK.value
        kint = int(k)

        path, scoretot = self._model.getDreamTeam(kint)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Il Dream Team con il minor tasso di sconfitta pari a {scoretot} è:"))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(p))
        self._view.update_page()