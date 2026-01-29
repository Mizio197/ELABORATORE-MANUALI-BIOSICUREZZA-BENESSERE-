import streamlit as st
from fpdf import FPDF
from fpdf.fonts import FontFace
from fpdf.enums import XPos, YPos
import os
import io

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="R-ADVISOR | Generatore Manuali", page_icon="📋", layout="wide")

# --- CLASSE PDF STYLE RELAZIONE ---
class PDF(FPDF):
    def __init__(self, client_name):
        super().__init__()
        self.client_name = client_name
        
    def header(self):
        # Logo Studio Summit a Destra
        if os.path.exists("assets/logo.png"):
            self.image("assets/logo.png", x=155, y=10, w=45)
        # Linea sottile sotto l'intestazione per pulizia
        self.set_draw_color(200, 200, 200)
        self.line(10, 35, 200, 35)
        self.ln(30)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 100, 100)
        # Testo a sinistra
        footer_text = f"ELABORATO CON R-ADVISOR-APP da STUDIO SUMMIT SRL per {self.client_name}"
        self.cell(0, 10, footer_text, align="L")
        # Numero pagina a destra
        self.set_x(-30)
        self.cell(0, 10, f"Pag. {self.page_no()}/{{nb}}", align="R")

    def chapter_title(self, label):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(0, 51, 102) # Blu scuro professionale
        self.cell(0, 10, label, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        self.ln(2)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 5, text, align='J', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(5)

    def sub_title(self, label):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(50, 50, 50)
        self.cell(0, 8, label, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')

# --- TESTI COMPLETI (DAI TUOI FILE) ---

TXT_POS_001 = """Scopo: Prevenire l'introduzione e la diffusione di agenti patogeni (virus, batteri, parassiti) all'interno dell'unità epidemiologica tramite vettori meccanici (veicoli, persone, attrezzature).
Riferimenti Normativi: Reg. UE 2016/429; Liste di controllo ClassyFarm/SNQBA.

1. Classificazione del Rischio Visitatori
Nelle more dell'analisi del rischio condotta per garantire una migliore efficacia delle attività di gestione ai fini della biosicurezza, si è provveduto a classificare gli stessi in differenti categorie:

Categoria A: Visitatori ad Alto Rischio (Professionali)
Soggetti che, per la natura della loro attività, frequentano regolarmente più allevamenti o hanno contatti diretti con animali.
Chi sono: Medici Veterinari, tecnici fecondatori, trasportatori di animali vivi, trasportatori di mangime (se entrano in zona pulita), tecnici manutentori di impianti zootecnici, pareggiatori, tosapecore, consulenti nutrizionisti.
Requisito specifico: Devono dichiarare preliminarmente all'accesso eventuali contatto con animali infetti, animali di nuova introduzione in altri allevamenti e, più in generale, altri fattori di rischio.

Categoria B: Visitatori a Medio/Basso Rischio
Soggetti che non hanno contatti frequenti con altri allevamenti o che non accederanno alle zone di stabulazione diretta.

2. Procedure di Ingresso
Tutti i visitatori devono attenersi alla seguente procedura rigorosa prima di accedere alla Zona Pulita:
- Annuncio: Suonare il campanello o contattare il personale. Attendere al cancello.
- Registrazione: Compilare il Registro Visitatori in ogni sua parte (inclusa dichiarazione "ultimo contatto").
- Vestizione: Indossare i DPI monouso o dedicati forniti dall'azienda (calzari, tuta/camice, cuffia) nella Zona Filtro.

3. Comportamento e Divieti
- È severamente vietato introdurre alimenti di origine animale.
- È vietato toccare gli animali se non espressamente autorizzati.
- Rispettare sempre il percorso "Marcia in Avanti" (dal pulito allo sporco)."""

TXT_POS_002 = """Scopo: Definire le modalità operative per l'introduzione di nuovi capi e per la gestione di animali residenti che manifestano segni clinici di malattia infettiva.
Riferimenti: Reg. UE 2016/429; Manuale ClassyFarm; Disciplinare SNQBA.

1. Definizione delle Aree
L'azienda identifica due aree funzionali distinte:
- Box di Quarantena (Nuovi Arrivi): Ubicato in area separata fisicamente dai gruppi di produzione. Mangiatoia e abbeveratoio dedicati.
- Box Infermeria (Animali Malati): Area dedicata a capi residenti che manifestano patologie (es. mastiti contagiose, zoppie gravi).

2. Procedura per Nuovi Ingressi
Ogni animale proveniente dall'esterno viene isolato per un periodo minimo o fino all'esito favorevole dei test sanitari.
Durante questo periodo:
- L'accudimento avviene per ultimo (a fine turno).
- Si utilizzano attrezzature dedicate o disinfettate dopo l'uso.

3. Gestione Letame
La lettiera rimossa dall'area quarantena/isolamento NON viene distribuita direttamente sui campi. Viene stoccata in un punto dedicato della concimaia per subire un processo di biotermizzazione (>60°C) per inattivare i patogeni.
Al termine del ciclo, il box subisce un vuoto sanitario dopo lavaggio e disinfezione."""

TXT_POS_003_TEMPLATE = """Scopo: Descrivere le misure di difesa passiva (Pest Proofing) e attiva (Pest Control) contro infestanti.
Riferimenti: Reg. (UE) 852/2004; Reg. (UE) 2016/429; SNQBA.

1. Responsabilità
La gestione è condivisa tra il Responsabile Biosicurezza (interno) e la ditta specializzata esterna STUDIO SUMMIT SRL (Iscritta ANID).

2. Monitoraggio e Interventi
La ditta specializzata esegue interventi di monitoraggio e controllo con frequenza {frequenza}.
Il numero di passaggi può essere intensificato in caso di infestazioni acute (superamento soglia di tolleranza).

3. Documentazione
- Planimetria Dispositivi: È presente e aggiornata una mappa planimetrica (vedi Allegati).
- Report di Intervento: Al termine di ogni visita, STUDIO SUMMIT SRL rilascia un rapporto indicante prodotti usati, consumi e catture.
- Schede di Sicurezza (SDS): Sono archiviate e disponibili le schede dei formulati.

4. Procedura di Emergenza
In caso di avvistamento massiccio tra un controllo e l'altro, l'operatore contatta immediatamente la ditta per un intervento straordinario."""

TXT_POS_004 = """Scopo: Garantire il rispetto dei fabbisogni fisiologici ed etologici dei bovini in conformità al Sistema di Qualità Nazionale per il Benessere Animale (SNQBA).
Riferimenti: D.Lgs 146/2001; D.Lgs 126/2011; Manuale ClassyFarm.

1. Formazione
Tutto il personale riceve formazione su manipolazione, riconoscimento segni di malattia e biosicurezza.
Gli animali vengono ispezionati almeno due volte al giorno.

2. Gestione Vitellaia
- Colostratura: Somministrazione di colostro (Brix >22%) entro le prime 6 ore.
- Decornazione: Entro 3-4 settimane con cauterizzazione termica, previa anestesia/analgesia.
- Code: È vietato il taglio della coda.

3. Monitoraggio Indicatori (Animal Based)
Si provvede al monitoraggio periodico di:
- Body Condition Score (BCS).
- Cleanliness Score (Pulizia).
- Locomotion Score (Zoppie).

4. Strutture ed Emergenze
Presenza di gruppo elettrogeno a riarmo automatico per ventilazione/mungitura e sistema di allarme."""

# --- DATI CHECKLIST (Ricostruita dal file Excel) ---
CHECKLIST_DATA = [
    ("Segnaletica", "Cartello divieto ingresso/norme biosicurezza presente al varco?"),
    ("Cancello", "Il varco di accesso è chiuso/presidiato?"),
    ("Parcheggio", "Auto visitatori parcheggiate in zona esterna (sporca)?"),
    ("Registro", "Registro Ingressi compilato in ogni parte?"),
    ("DPI", "Disponibili calzari/camici per visitatori?"),
    ("Pest Control", "Erogatori integri e fissati al muro?"),
    ("Pest Control", "Cartellino di segnalazione presente sopra le trappole?"),
    ("Vitelli", "Acqua presente e pulita nei box?"),
    ("Vitelli", "Contatto visivo garantito tra vitelli <8 settimane?"),
    ("Farmaci", "Armadietto farmaci chiuso a chiave?"),
    ("Documenti", "Report STUDIO SUMMIT SRL archiviati e disponibili?")
]

# --- INTERFACCIA UTENTE ---
st.title("Generatore Manuali | STUDIO SUMMIT")

with st.form("main_form"):
    st.subheader("1. Anagrafica Cliente")
    col1, col2 = st.columns(2)
    with col1:
        ragione_sociale = st.text_input("Ragione Sociale")
        indirizzo = st.text_input("Indirizzo")
        codice_stalla = st.text_input("Codice Stalla")
    with col2:
        piva = st.text_input("Partita IVA")
        telefono = st.text_input("Telefono")
        email = st.text_input("Email")

    st.subheader("2. Responsabili")
    c_resp1, c_resp2 = st.columns(2)
    resp_bio = c_resp1.text_input("Resp. Biosicurezza")
    resp_ben = c_resp2.text_input("Resp. Benessere")
    data_corso = c_resp2.date_input("Data Attestato Benessere")

    st.subheader("3. Variabili POS & Allegati")
    freq_pest = st.selectbox("Frequenza Pest Control", ["quadrimestrale", "bimestrale", "mensile", "trimestrale"])
    uploaded_planimetria = st.file_uploader("Carica Planimetria Trappole (JPG/PNG)", type=["jpg", "png", "jpeg"])

    submitted = st.form_submit_button("GENERA PDF")

# --- LOGICA GENERAZIONE ---
if submitted:
    if not ragione_sociale:
        st.error("Inserire Ragione Sociale!")
    else:
        try:
            pdf = PDF(ragione_sociale)
            pdf.alias_nb_pages()
            pdf.set_auto_page_break(auto=True, margin=15)
            
            # --- COPERTINA ---
            pdf.add_page()
            pdf.ln(50)
            pdf.set_font("Helvetica", "B", 24)
            pdf.multi_cell(0, 10, "MANUALE DI CORRETTA PRASSI\nPER BENESSERE E BIOSICUREZZA", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(10)
            
            if os.path.exists("assets/cover.jpg"):
                x_pos = (pdf.w - 140) / 2
                pdf.image("assets/cover.jpg", x=x_pos, w=140)
            
            pdf.ln(20)
            pdf.set_font("Helvetica", "B", 18)
            pdf.cell(0, 10, ragione_sociale, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font("Helvetica", "", 12)
            pdf.cell(0, 10, f"Codice Stalla: {codice_stalla}", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            # --- PAGINA ANAGRAFICA ---
            pdf.add_page()
            pdf.chapter_title("SCHEDA ANAGRAFICA")
            
            # Tabella Anagrafica semplice con celle
            pdf.set_font("Helvetica", "", 11)
            data = [
                ("Ragione Sociale:", ragione_sociale),
                ("Indirizzo:", indirizzo),
                ("P.IVA:", piva),
                ("Codice Stalla:", codice_stalla),
                ("Contatti:", f"{telefono} {email}"),
                ("Resp. Biosicurezza:", resp_bio),
                ("Resp. Benessere:", resp_ben),
                ("Data Corso:", data_corso.strftime("%d/%m/%Y"))
            ]
            
            for key, val in data:
                pdf.set_font("Helvetica", "B", 11)
                pdf.cell(50, 8, key, border=1)
                pdf.set_font("Helvetica", "", 11)
                pdf.cell(0, 8, str(val), border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            # --- POS 001 ---
            pdf.add_page()
            pdf.chapter_title("POS 001 - VISITATORI")
            pdf.body_text(TXT_POS_001)

            # --- POS 002 ---
            pdf.add_page()
            pdf.chapter_title("POS 002 - QUARANTENA")
            pdf.body_text(TXT_POS_002)

            # --- POS 003 ---
            pdf.add_page()
            pdf.chapter_title("POS 003 - PEST MANAGEMENT")
            pdf.body_text(TXT_POS_003_TEMPLATE.format(frequenza=freq_pest))

            # --- POS 004 ---
            pdf.add_page()
            pdf.chapter_title("POS 004 - BENESSERE")
            pdf.body_text(TXT_POS_004)

            # --- ALLEGATI ---
            pdf.add_page()
            pdf.chapter_title("ALLEGATI")
            
            # 1. Cartello
            pdf.sub_title("1. Cartello Biosicurezza")
            if os.path.exists("assets/cartello.jpg"):
                pdf.image("assets/cartello.jpg", w=160, x=25)
            else:
                pdf.body_text("[Immagine Cartello non trovata]")
            
            # 2. Planimetria
            pdf.add_page()
            pdf.sub_title("2. Planimetria Pest Control")
            if uploaded_planimetria:
                # Salva temporaneamente il file caricato
                with open("temp_plan.jpg", "wb") as f:
                    f.write(uploaded_planimetria.getbuffer())
                pdf.image("temp_plan.jpg", w=170, x=20)
            else:
                pdf.body_text("[Nessuna Planimetria Caricata]")

            # 3. BCS
            pdf.add_page()
            pdf.sub_title("3. Infografica BCS")
            if os.path.exists("assets/bcs.jpg"):
                pdf.image("assets/bcs.jpg", w=170, x=20)
            else:
                pdf.body_text("[Immagine BCS non trovata]")

            # --- CHECKLIST FINALE ---
            pdf.add_page()
            pdf.chapter_title("CHECK LIST DI MONITORAGGIO")
            pdf.body_text("Da compilare con cadenza periodica.")
            pdf.ln(5)
            
            # Intestazione Tabella
            pdf.set_fill_color(240, 240, 240)
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(40, 8, "Ambito", 1, 0, 'C', fill=True)
            pdf.cell(110, 8, "Controllo", 1, 0, 'C', fill=True)
            pdf.cell(40, 8, "Esito (C/NC)", 1, 1, 'C', fill=True) # 1 finale va a capo
            
            # Righe
            pdf.set_font("Helvetica", "", 10)
            for area, check in CHECKLIST_DATA:
                pdf.cell(40, 8, area, 1)
                pdf.cell(110, 8, check, 1)
                pdf.cell(40, 8, "", 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            # --- OUTPUT ---
            # Metodo più sicuro per Streamlit: output su bytearray
            pdf_bytes = pdf.output()
            
            st.success("✅ Documento generato con successo!")
            st.download_button(
                label="📥 SCARICA PDF FINALE",
                data=pdf_bytes,
                file_name=f"Manuale_{ragione_sociale.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
            
        except Exception as e:
            st.error(f"Si è verificato un errore durante la generazione: {e}")
