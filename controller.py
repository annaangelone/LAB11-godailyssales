import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []

    def fillDD(self):
        years = [2015, 2016, 2017, 2018]

        for year in years:
            self._listYear.append(year)
            self._view._ddyear.options.append(ft.dropdown.Option(year))

        self._listColor = self._model._colors

        for c in self._listColor:
            self._view._ddcolor.options.append(ft.dropdown.Option(c))

    def handle_graph(self, e):
        colore = self._view._ddcolor.value
        anno = self._view._ddyear.value

        if colore is None:
            self._view.create_alert('No color selected, please select a color')
            return

        if anno is None:
            self._view.create_alert('No year selected, please select an year')
            return

        self._model.buildGraph(colore, anno)
        self._view.txtOut.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txtOut.controls.append(ft.Text(f"Il grafo contiene {self._model.getNumNodes()} nodi."))
        self._view.txtOut.controls.append(ft.Text(f"Il grafo contiene {self._model.getNumEdges()} archi."))

        archiBest = self._model.getArchiPesoMaggiore()

        for a in archiBest:
            self._view.txtOut.controls.append(ft.Text(f"Arco da {a[0]} a {a[1]}, peso={a[2]}"))

        nodiRipetuti, volte = self._model.getNumberOne(archiBest)

        self._view.txtOut.controls.append(ft.Text(f"I nodi ripetuti sono: {nodiRipetuti}, conto={volte}"))

        self._view.btn_search.disabled = False
        self.fillDDProduct()

        self._view.update_page()


    def fillDDProduct(self):
        prodotti = self._model._prodotti

        for p in prodotti:
            self._view._ddnode.options.append(ft.dropdown.Option(p.Product_number))


    def handle_search(self, e):
        prodotto = int(self._view._ddnode.value)

        if prodotto is None:
            self._view.create_alert("No product selected, please select a product")
            return

        path, lun = self._model.getPercorso(prodotto)

        self._view.txtOut2.controls.append(ft.Text(f"Numero archi percorso più lungo: {lun}"))

        for i in range(len(path) - 1):
            self._view.txtOut2.controls.append(ft.Text(f"{path[i]} --> {path[i+1]}; peso={self._model.getPeso(path[i], path[i+1])}"))

        self._view.update_page()
