import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    # TODO
    tipo = ft.TextField(value = "",  label="Tipo")
    marca = ft.TextField(value = "", label="Marca")
    anno = ft.TextField(value = "", label="Anno")

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    # TODO
    def conferma_nuovo_strumento(e):
        if anno.value.isdigit():
            if tipo.value and marca.value and anno.value and txtOut.value:
                tipoDaAgg = tipo.value
                marcaDaAgg = marca.value
                annoDaAgg = anno.value
                txtOutDaAgg = txtOut.value
                strumento_nuovo = deposito.aggiungi_strumento(tipoDaAgg, marcaDaAgg, annoDaAgg ,txtOutDaAgg)
                aggiorna_lista_strumenti()
                #svuoto i textFields
                tipo.value =""
                marca.value =""
                anno.value =""
                txtOut.value = 0
            else:
                alert.show_alert("❌ Errore: Inserire i dati mancanti")
        else:
            alert.show_alert("❌ Errore: Inserire un valore valido per l'anno")

    def handleAdd(e):
        current_val = txtOut.value
        txtOut.value = float(current_val) + 1      #il pulsante permette di cambiare il prezzo di 1€ per ogni click: potrebbe risultare lento, ma basta modificare questa riga e la riga 78
        txtOut.update()

    def handleRemove(e):
        current_val = txtOut.value
        if current_val > 0:
            txtOut.value = float(current_val) - 1
            txtOut.update()
        else:
            alert.show_alert("❌ Errore: Non è possibile avere un prezzo negativo")


    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    # TODO
    pulsante_conferma_nuovo_strumento = ft.Button("Aggiungi strumento", on_click=conferma_nuovo_strumento)


    btnMinus = ft.IconButton(icon=ft.Icons.REMOVE,
                             icon_color="red",
                             icon_size=24, on_click=handleRemove)
    btnAdd = ft.IconButton(icon=ft.Icons.ADD,
                           icon_color="green",
                           icon_size=24, on_click=handleAdd)
    txtOut = ft.TextField(width=100, disabled=True,
                          value=0,
                          border={
                              ft.ControlState.DEFAULT: ft.OutlineInputBorder(
                                  side=ft.BorderSide(color="grey", width=1)),
                              ft.ControlState.DISABLED: ft.OutlineInputBorder(
                                  side=ft.BorderSide(color="grey", width=1))
                          },
                          text_align=ft.TextAlign.CENTER)


    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO
        ft.Text("Aggiungi nuovo strumento"),
        ft.Row(spacing=10,
               controls = [ tipo, marca, anno, btnMinus, txtOut, btnAdd],
               alignment=ft.MainAxisAlignment.CENTER),

        ft.Row(controls = [pulsante_conferma_nuovo_strumento],
               alignment = ft.MainAxisAlignment.CENTER),

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
