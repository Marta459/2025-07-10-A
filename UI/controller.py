import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillddcategory(self):
        for categoria in self._model.getCategorie():
            self._view.ddcategory.options.append(
                ft.dropdown.Option(key=str(categoria["category_id"]), text=categoria["category_name"])
            )


    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        start_date = self._view.dp1.value
        end_date = self._view.dp2.value
        categoria = self._view.ddcategory.value

        if start_date is None or end_date is None:
            self._view.txt_result.controls.append(ft.Text("Seleziona entrambe le date", color="red"))
            self._view.update_page()
            return

        if categoria is None:
            self._view.txt_result.controls.append(ft.Text("Seleziona una categoria", color="red"))
            self._view.update_page()
            return

        if start_date > end_date:
            self._view.txt_result.controls.append(
                ft.Text("La data di inizio deve precedere quella di fine", color="red"))
            self._view.update_page()
            return

        try:
            categoria_id = int(categoria)
            num_nodi,num_archi = self._model.creaGrafo(categoria,start_date, end_date)
            self._view.txt_result.controls.append(ft.Text(f"Start date: {start_date.date()}"))
            self._view.txt_result.controls.append(ft.Text(f"End date: {end_date.date()}"))
            self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:", color="red"))
            self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {num_nodi}"))
            self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {num_archi}"))
            self._view.update_page()

        except Exception as ex:
            self._view.txt_result.controls.append(ft.Text(f"Errore durante la creazione del grafo: {ex}", color="red"))
            self._view.update_page()

    def handleBestProdotti(self, e):
        if self._model.getGrafo() is None:
            self._view.txt_result.controls.append(ft.Text("Devi prima creare il grafo", color="red"))
            self._view.update_page()
            return

        try:
            migliori = self._model.getMigliori5()
            self._view.txt_result.controls.append(ft.Text("I cinque prodotti più venduti sono:"))
            for id_prodotto, punteggio in migliori:
                prodotto = self._model.getProdottoDati(id_prodotto)
                testo = f"{prodotto['product_name']} with score {punteggio}"
                self._view.txt_result.controls.append(ft.Text(testo))
            self._view.update_page()
        except Exception as ex:
            self._view.txt_result.controls.append(ft.Text(f"Errore: {ex}", color="red"))
            self._view.update_page()

    def handleCercaCammino(self, e):
        pass



    def setDates(self):
        first, last = self._model.getDateRange()

        self._view.dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view.dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp2.current_date = datetime.date(last.year, last.month, last.day)
