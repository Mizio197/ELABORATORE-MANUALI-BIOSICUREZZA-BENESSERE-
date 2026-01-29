import streamlit as st
from fpdf import FPDF
from fpdf.fonts import FontFace # Import necessario per la correzione
import os
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="R-ADVISOR | Generatore Manuali", page_icon="📋", layout="wide")

# --- CLASSE PDF GENERATOR ---
class PDF(FPDF):
    def __init__(self, client_name):
        super().__init__()
        self.client_name = client_name
        
    def header(self):
        # Logo Studio Summit a Destra
        if os.path.exists("assets/logo.png"):
            # x=150 (destra), y=8, w=50 (larghezza)
            self.image("assets/logo.png", x=150, y=8, w=50)
        self.ln(20) # Spazio dopo il logo

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(128)
        # Piè di pagina personalizzato
        footer_text = f"ELABORATO CON R-ADVISOR-APP da STUDIO SUMMIT SRL per {self.client_name} | Pagina {self.page_no()}/{{nb}}"
        self.cell(0, 10, footer_text, align="C")

    def section_title(self, label):
        self.set_font("Arial", "B", 14)
        self.set_text_color(0, 51, 102) # Un blu scuro professionale
        self.cell(0, 10, label, ln=True, align='L')
        self.ln(2)

    def section_body(self, text):
        self.set_font("Arial", "", 11)
        self.set_text_color(0)
        self.multi_cell(0, 6, text, align='J') # J = Justified
        self.ln(5)

# --- TESTI STATICI (POS) ---

TEXT_POS_001 = """Scopo: Prevenire l'introduzione e la diffusione di agenti patogeni all'interno dell'unità epidemiologica tramite vettori meccanici.
Riferimenti Normativi: Reg. UE 2016/429; Liste di controllo ClassyFarm/SNQBA.

1. Classificazione del Rischio Visitatori
I visitatori sono classificati in:
Categoria A (Alto Rischio): Veterinari, tecnici, trasportatori. Devono dichiarare contatti recenti con altri animali.
Categoria B (Medio/Basso Rischio): Visitatori senza contatti diretti con animali.

2. Procedure di Ingresso
Tutti i visitatori devono:
- Annunciare la propria presenza e firmare il Registro Ingressi.
- Indossare i DPI forniti (calzari, camici, cuffie) nella Zona Filtro.
- Rispettare i percorsi indicati (Marcia in Avanti: dal pulito allo sporco).

3. Divieti
È vietato introdurre cibo nelle aree di stabulazione e toccare gli animali se non autorizzati."""

TEXT_POS_002 = """Scopo: Definire le modalità per l'introduzione di nuovi capi e la gestione degli animali malati.
Riferimenti: Reg. UE 2016/429; Manuale ClassyFarm.

1. Box di Quarantena (Nuovi Arrivi)
Area separata fisicamente dai gruppi di produzione. Mangiatoia e abbeveratoio dedicati.
Procedura:
- Controllo documentale e sanitario all'arrivo.
- Isolamento per il periodo necessario agli accertamenti sierologici.

2. Box Infermeria (Animali Malati)
Area dedicata a capi che manifestano patologie.
Gestione:
- Lettiera pulita e asciutta, facile accesso all'acqua.
- Accesso consentito solo agli addetti autorizzati.
- Al termine dell'uso: svuotamento, lavaggio, disinfezione e vuoto sanitario.

3. Gestione Letame
La lettiera della quarantena viene stoccata separatamente per biotermizzazione (>60°C) prima dello spandimento."""

TEXT_POS_003_TEMPLATE = """Scopo: Descrivere le misure di difesa passiva (Pest Proofing) e attiva (Pest Control) contro infestanti.
Riferimenti: Reg. (UE) 852/2004; SNQBA.

1. Responsabilità
La gestione è condivisa tra il Responsabile Biosicurezza (interno) e la ditta specializzata STUDIO SUMMIT SRL.

2. Monitoraggio e Interventi
La ditta esterna effettua interventi con frequenza {frequenza}.
Al termine di ogni visita, viene rilasciato un report con:
- Prodotti utilizzati e schede di sicurezza.
- Esito del monitoraggio (consumi, catture).
- Eventuali Non Conformità rilevate.

3. Planimetria e Dispositivi
È presente una mappa planimetrica (Allegato) che identifica la posizione delle trappole. I dispositivi sono numerati e fissati.

4. Procedura di Emergenza
In caso di avvistamento massiccio tra un controllo e l'altro, l'operatore contatta immediatamente la ditta per un intervento straordinario."""

TEXT_POS_004 = """Scopo: Garantire il rispetto dei fabbisogni etologici e fisiologici dei bovini.
Riferimenti: D.Lgs 146/2001; SNQBA.

1. Formazione
Tutto il personale riceve formazione su manipolazione e riconoscimento segni di malattia. Ispezione capi almeno 2 volte al giorno.

2. Gestione Vitellaia
- Colostratura entro 6 ore (Brix >22%).
- Decornazione: entro 3-4 settimane con anestesia/analgesia.
- Divieto di taglio della coda.

3. Monitoraggio Indicatori (Animal Based)
Si provvede al monitoraggio periodico di:
- Body Condition Score (BCS).
- Cleanliness Score (Pulizia).
- Locomotion Score (Zoppie).

4. Strutture e Emergenze
Presenza di gruppo elettrogeno a riarmo automatico e sistema di allarme per ventilazione/mungitura."""

# --- INTERFACCIA UTENTE (SIDEBAR & FORM) ---
st.title("Generatore Manuale Biosicurezza & Benessere")
st.markdown("Compila i dati aziendali per generare il PDF personalizzato secondo lo standard **Studio Summit**.")

with st.form("data_entry_form"):
    st.header("1. Anagrafica Azienda")
    col1, col2 = st.columns(2)
    
    with col1:
        ragione_sociale = st.text_input("Ragione Sociale Azienda", placeholder="Es. Az. Agr. Rossi Mario")
        indirizzo = st.text_input("Indirizzo Sede Operativa")
        codice_stalla = st.text_input("Codice Stalla (ASL)")
    
    with col2:
        piva = st.text_input("P.IVA / Codice Fiscale")
        telefono = st.text_input("Telefono / Cellulare")
        email = st.text_input("Email")

    st.header("2. Responsabili")
    c_resp1, c_resp2 = st.columns(2)
    with c_resp1:
        resp_bio = st.text_input("Responsabile Biosicurezza (Nome e Cognome)")
    with c_resp2:
        resp_ben = st.text_input("Responsabile Benessere (Nome e Cognome)")
        data_corso_ben = st.date_input("Data Rilascio Attestato Corso Benessere")

    st.header("3. Personalizzazione POS")
    freq_pest = st.selectbox(
        "Frequenza controlli Pest Control (Ditta Esterna)",
        options=["quadrimestrale", "bimestrale", "mensile", "trimestrale"],
        index=0,
        help="Questo modificherà automaticamente il testo nella POS 003"
    )

    st.header("4. Allegati Variabili")
    st.markdown("Carica qui la **Planimetria Pest Control** specifica per questo cliente.")
    uploaded_planimetria = st.file_uploader("Trascina qui il file (JPG/PNG)", type=["jpg", "jpeg", "png"])

    submitted = st.form_submit_button("GENERA MANUALE PDF")

# --- LOGICA DI GENERAZIONE ---
if submitted:
    if not ragione_sociale:
        st.error("Inserire almeno la Ragione Sociale per procedere.")
    else:
        # Inizializza PDF
        pdf = PDF(ragione_sociale)
        pdf.alias_nb_pages()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # --- COPERTINA ---
        pdf.add_page()
        # Titolo Copertina
        pdf.ln(30)
        pdf.set_font("Arial", "B", 24)
        pdf.cell(0, 10, "MANUALE DI CORRETTA PRASSI", align="C", ln=True)
        pdf.cell(0, 10, "PER BENESSERE E BIOSICUREZZA", align="C", ln=True)
        pdf.ln(10)
        
        # Immagine Copertina (Centrata)
        if os.path.exists("assets/cover.jpg"):
            # Calcolo posizione x per centrare un'immagine larga 150
            page_width = pdf.w
            img_width = 150
            x_pos = (page_width - img_width) / 2
            pdf.image("assets/cover.jpg", x=x_pos, w=img_width)
        
        pdf.ln(15)
        # Nome Azienda in Copertina
        pdf.set_font("Arial", "B", 20)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 10, ragione_sociale, align="C", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Codice Stalla: {codice_stalla}", align="C", ln=True)

        # --- PAGINA ANAGRAFICA ---
        pdf.add_page()
        pdf.section_title("SCHEDA ANAGRAFICA E RESPONSABILITÀ")
        
        pdf.set_font("Arial", "", 12)
        info_data = [
            ("Ragione Sociale", ragione_sociale),
            ("Indirizzo", indirizzo),
            ("Codice Stalla", codice_stalla),
            ("P.IVA/CF", piva),
            ("Contatti", f"{telefono} - {email}"),
            ("", ""), # Spazio vuoto
            ("Responsabile Biosicurezza", resp_bio),
            ("Responsabile Benessere", resp_ben),
            ("Data Attestato Benessere", data_corso_ben.strftime("%d/%m/%Y"))
        ]
        
        # TABELLA CORRETTA CON FontFace
        with pdf.table() as table:
            for row in info_data:
                r = table.row()
                # Uso FontFace per il grassetto invece della stringa "B"
                r.cell(row[0], style=FontFace(emphasis="BOLD")) 
                r.cell(row[1])

        # --- POS 001 VISITATORI ---
        pdf.add_page()
        pdf.section_title("POS 001 - GESTIONE E REGOLE VISITATORI ESTERNI")
        pdf.section_body(TEXT_POS_001)

        # --- POS 002 QUARANTENA ---
        pdf.add_page()
        pdf.section_title("POS 002 - GESTIONE E REGOLE QUARANTENA")
        pdf.section_body(TEXT_POS_002)

        # --- POS 003 PEST MANAGEMENT (DINAMICO) ---
        pdf.add_page()
        pdf.section_title("POS 003 - GESTIONE E REGOLE PEST MANAGEMENT")
        # Sostituzione dinamica della frequenza
        testo_dinamico_pos3 = TEXT_POS_003_TEMPLATE.format(frequenza=freq_pest)
        pdf.section_body(testo_dinamico_pos3)

        # --- POS 004 BENESSERE ---
        pdf.add_page()
        pdf.section_title("POS 004 - GESTIONE E REGOLE BENESSERE ANIMALE")
        pdf.section_body(TEXT_POS_004)

        # --- SEZIONE ALLEGATI ---
        pdf.add_page()
        pdf.section_title("ALLEGATI")
        pdf.ln(5)

        # 1. Cartello Visitatori
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "1. CARTELLO NORME BIOSICUREZZA (Da esporre all'ingresso)", ln=True)
        if os.path.exists("assets/cartello.jpg"):
            pdf.image("assets/cartello.jpg", w=160, x=25)
        pdf.ln(10)

        # 2. Planimetria (Caricata dall'utente)
        pdf.add_page()
        pdf.cell(0, 10, "2. PLANIMETRIA PEST CONTROL (Mappa Trappole)", ln=True)
        if uploaded_planimetria:
            # Salvataggio temporaneo per FPDF
            temp_path = "temp_planimetria.jpg"
            with open(temp_path, "wb") as f:
                f.write(uploaded_planimetria.getbuffer())
            pdf.image(temp_path, w=170, x=20)
        else:
            pdf.set_font("Arial", "I", 10)
            pdf.cell(0, 10, "[Nessuna planimetria caricata in fase di generazione]", ln=True)
        
        # 3. Infografica BCS
        pdf.add_page()
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "3. INFOGRAFICA BODY CONDITION SCORE (BCS)", ln=True)
        if os.path.exists("assets/bcs.jpg"):
            pdf.image("assets/bcs.jpg", w=170, x=20)

        # Output del file
        pdf_filename = f"Manuale_Biosicurezza_{ragione_sociale.replace(' ', '_')}.pdf"
        
        # Salvataggio byte array per il download
        pdf_bytes = pdf.output()
        
        st.success("✅ Manuale generato con successo!")
        
        st.download_button(
            label="📥 SCARICA MANUALE PDF",
            data=pdf_bytes,
            file_name=pdf_filename,
            mime="application/pdf"
        )
