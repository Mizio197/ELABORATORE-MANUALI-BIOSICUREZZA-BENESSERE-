import streamlit as st
from fpdf import FPDF
from fpdf.fonts import FontFace
from fpdf.enums import XPos, YPos
import os

# --- CONFIGURAZIONE PAGINA STREAMLIT ---
st.set_page_config(page_title="R-ADVISOR | Generatore Manuali", page_icon="📋", layout="wide")

# --- CLASSE PDF AVANZATA (Stile Relazione Tecnica) ---
class PDF(FPDF):
    def __init__(self, client_name, reason_social):
        super().__init__()
        self.client_name = client_name
        self.reason_social = reason_social
        
    def header(self):
        # Logo Studio Summit a Destra (Alto)
        if os.path.exists("assets/logo.png"):
            # Posizionato a destra, larghezza 45mm
            self.image("assets/logo.png", x=155, y=10, w=45)
        
        # Linea separatrice header (opzionale, per pulizia grafica)
        self.set_y(30)
        # self.line(10, 30, 200, 30) 

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 100, 100) # Grigio scuro
        
        # Testo Piè di pagina
        footer_text = f"ELABORATO CON R-ADVISOR-APP da STUDIO SUMMIT SRL per {self.reason_social}"
        page_num = f"Pagina {self.page_no()} di {{nb}}"
        
        # Cella sinistra (Testo)
        self.cell(0, 10, footer_text, align="L")
        # Cella destra (Numero pagina)
        self.set_x(-30)
        self.cell(0, 10, page_num, align="R")

    def section_title(self, label):
        """Titoli di sezione stile report tecnico (Grassetto, Spaziato)"""
        self.ln(10)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(0, 0, 0) # Nero
        self.cell(0, 10, label.upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        self.ln(2)

    def paragraph(self, text):
        """Paragrafo con testo giustificato e interlinea leggibile"""
        self.set_font("Helvetica", "", 11)
        self.set_text_color(20, 20, 20) # Nero morbido
        self.multi_cell(0, 6, text, align='J', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(3)

    def sub_title(self, label):
        """Sottotitoli per i paragrafi interni"""
        self.ln(3)
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 6, label, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')

# --- DEFINIZIONE TESTI COMPLETI (DAI TUOI FILE) ---

TXT_POS_001 = """Scopo: Prevenire l'introduzione e la diffusione di agenti patogeni (virus, batteri, parassiti) all'interno dell'unità epidemiologica tramite vettori meccanici (veicoli, persone, attrezzature).
Riferimenti Normativi: Reg. UE 2016/429; Liste di controllo ClassyFarm/SNQBA.

1. CLASSIFICAZIONE DEL RISCHIO VISITATORI
Nelle more dell’analisi del rischio condotta per garantire una migliore efficacia delle attività di gestione ai fini della biosicurezza, si è provveduto a classificare gli stessi in differenti categorie:

Categoria A: Visitatori ad Alto Rischio (Professionali)
Soggetti che, per la natura della loro attività, frequentano regolarmente più allevamenti o hanno contatti diretti con animali.
Chi sono: Medici Veterinari, tecnici fecondatori, trasportatori di animali vivi, trasportatori di mangime (se entrano in zona pulita), tecnici manutentori di impianti zootecnici, pareggiatori, tosapecore, consulenti nutrizionisti.
Requisito specifico: Devono dichiarare preliminarmente all’accesso eventuali contatto con animali infetti, animali di nuova introduzione in altri allevamenti e, più in generale, altri fattori di rischio, anche solo potenziale.

Categoria B: Visitatori a Medio/Basso Rischio
Soggetti che non hanno contatti frequenti con altri allevamenti o che non accederanno alle zone di stabulazione diretta.

2. PROCEDURE DI INGRESSO (ZONA FILTRO)
Tutti i visitatori, indipendentemente dalla categoria, devono attenersi alla seguente procedura rigorosa prima di accedere alla Zona Pulita (area di allevamento):
- Annuncio: Suonare il campanello o contattare il personale telefonicamente. Attendere al cancello.
- Registrazione: Compilare il Registro Visitatori in ogni sua parte.
- Vestizione: Indossare i DPI monouso o dedicati forniti dall'azienda (calzari, tuta/camice, cuffia).

3. COMPORTAMENTO E DIVIETI
- È severamente vietato introdurre alimenti di origine animale.
- È vietato toccare gli animali se non espressamente autorizzati.
- Rispettare sempre il percorso "Marcia in Avanti" (dal pulito allo sporco)."""

TXT_POS_002 = """Scopo: Definire le modalità operative per l'introduzione di nuovi capi (acclimatamento e controllo sanitario) e per la gestione di animali residenti che manifestano segni clinici di malattia infettiva.
Riferimenti: Reg. UE 2016/429 (Animal Health Law); Manuale ClassyFarm; Disciplinare SNQBA.

1. DEFINIZIONE DELLE AREE
L'azienda identifica due aree funzionali distinte:
- Box di Quarantena (Nuovi Arrivi): Ubicato in area separata fisicamente dai gruppi di produzione. Mangiatoia e abbeveratoio dedicati.
- Box Infermeria/Isolamento (Animali Malati): Area dedicata a capi residenti che manifestano patologie (es. mastiti contagiose, zoppie gravi infette).

2. PROCEDURA PER NUOVI INGRESSI
Ogni animale proveniente dall'esterno viene isolato per un periodo minimo (es. 21-28 giorni) o fino all'esito favorevole dei test sierologici.
Durante questo periodo:
- L'accudimento avviene per ultimo (a fine turno).
- Si utilizzano attrezzature dedicate (pale, forche, secchi) o disinfettate dopo l'uso.

3. GESTIONE LETAME E PULIZIA
La lettiera rimossa dall'area quarantena/isolamento NON viene distribuita direttamente sui campi. Viene stoccata in un punto dedicato della concimaia per subire un processo di biotermizzazione (>60°C) per inattivare i patogeni.
Al termine del ciclo (guarigione o spostamento), il box subisce un vuoto sanitario dopo lavaggio e disinfezione."""

# Nota: Qui useremo .format() per la frequenza dinamica
TXT_POS_003_TEMPLATE = """Scopo: Descrivere le misure di difesa passiva (Pest Proofing) e attiva (Pest Control) messe in atto dall'azienda per controllare la presenza di roditori, insetti e altri animali indesiderati.
Riferimenti: Reg. (UE) 852/2004; Reg. (UE) 2016/429; SNQBA.

1. RESPONSABILITÀ
La gestione del piano di lotta agli infestanti è suddivisa tra il personale interno (Responsabile Biosicurezza) e una ditta specializzata esterna.
Ditta Specializzata: STUDIO SUMMIT SRL (Iscritta ANID).

2. MONITORAGGIO E FREQUENZA
La ditta specializzata esegue interventi di monitoraggio e controllo con frequenza {frequenza}.
Il numero di passaggi può essere intensificato in caso di infestazioni acute (superamento soglia di tolleranza).

3. DOCUMENTAZIONE E PLANIMETRIA
- Planimetria Dispositivi: È presente e aggiornata una mappa planimetrica dell'azienda (vedi Sezione Allegati) che identifica univocamente la posizione di ogni erogatore.
- Report di Intervento: Al termine di ogni visita, STUDIO SUMMIT SRL rilascia un rapporto indicante prodotti usati, consumi rilevati e catture.
- Schede di Sicurezza (SDS): Sono archiviate e disponibili le schede di tutti i formulati chimici impiegati.

4. PROCEDURA DI EMERGENZA
Qualora il personale aziendale rilevi la presenza di infestanti tra un controllo e l'altro, contatta immediatamente la ditta per un intervento straordinario entro i tempi contrattuali."""

TXT_POS_004 = """Scopo: Garantire il rispetto dei fabbisogni fisiologici ed etologici dei bovini in tutte le fasi di allevamento, in conformità al Sistema di Qualità Nazionale per il Benessere Animale (SNQBA).
Riferimenti: D.Lgs 146/2001; D.Lgs 126/2011; Manuale ClassyFarm.

1. FORMAZIONE E COMPETENZA
Tutto il personale riceve formazione adeguata sulla manipolazione degli animali, sul riconoscimento dei segni di malattia e sui principi di biosicurezza.
Gli animali vengono ispezionati almeno due volte al giorno.

2. GESTIONE VITELLAIA
- Colostratura: Somministrazione di colostro di alta qualità (Brix >22%) entro le prime 6 ore di vita.
- Decornazione: Eseguita entro la 3a-4a settimana con cauterizzazione termica, previa anestesia locale e analgesia (FANS).
- Code: È vietato il taglio della coda (caudectomia).

3. MONITORAGGIO INDICATORI (ANIMAL BASED)
Si provvede al monitoraggio periodico (es. tramite ClassyFarm) di:
- Body Condition Score (BCS): Per valutare lo stato nutrizionale.
- Cleanliness Score: Per valutare l'igiene.
- Locomotion Score: Per rilevare precocemente zoppie.

4. STRUTTURE ED EMERGENZE
L'azienda è dotata di gruppo elettrogeno a riarmo automatico per garantire il funzionamento di mungitura e ventilazione in caso di blackout. È presente un sistema di allarme."""

# --- DATI CHECKLIST (Ricostruita dal CSV) ---
CHECKLIST_DATA = [
    ["Punto di Controllo", "Requisito da Verificare", "Esito (C/NC)"],
    ["Segnaletica", "Il cartello norme biosicurezza è presente e leggibile all'ingresso?", ""],
    ["Cancello/Sbarra", "Il varco di accesso è chiuso per impedire ingressi non autorizzati?", ""],
    ["Parcheggio", "Le auto visitatori sono nel parcheggio esterno (Zona Sporca)?", ""],
    ["Registro", "Il Registro Ingressi è compilato in ogni parte?", ""],
    ["DPI", "Sono disponibili calzari, camici e cuffie per i visitatori?", ""],
    ["Infermeria", "I box isolamento sono puliti e con lettiera adeguata?", ""],
    ["Pest Control", "Gli erogatori sono integri e fissati al muro?", ""],
    ["Pest Control", "È presente il cartellino di segnalazione sopra le trappole?", ""],
    ["Vitelli", "L'acqua è presente e pulita nei box vitelli?", ""],
    ["Vitelli", "I vitelli <8 settimane hanno contatto visivo tra loro?", ""],
    ["Farmaci", "L'armadietto farmaci è chiuso a chiave?", ""],
    ["Documenti", "I report di STUDIO SUMMIT SRL sono archiviati?", ""]
]

# --- INTERFACCIA STREAMLIT ---
st.title("Generatore Manuali | STUDIO SUMMIT")
st.markdown("**Creazione Manuale Corretta Prassi (Biosicurezza e Benessere)**")

# CSS per nascondere menu standard e rendere l'app più pulita
st.markdown("""
<style>
    .reportview-container { margin-top: -2em; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

with st.form("main_form"):
    col_logo, col_info = st.columns([1, 3])
    with col_logo:
        st.image("assets/logo.png", width=150) if os.path.exists("assets/logo.png") else st.write("Logo non trovato")
    
    with col_info:
        st.subheader("Dati Aziendali")
        ragione_sociale = st.text_input("Ragione Sociale Completa")
        indirizzo = st.text_input("Indirizzo Sede")
        codice_stalla = st.text_input("Codice Stalla (es. 001AV123)")
        piva = st.text_input("Partita IVA")

    st.markdown("---")
    
    col_resp1, col_resp2, col_freq = st.columns(3)
    with col_resp1:
        resp_bio = st.text_input("Resp. Biosicurezza (Nome Cognome)")
    with col_resp2:
        resp_ben = st.text_input("Resp. Benessere (Nome Cognome)")
        data_corso = st.date_input("Data Attestato Benessere")
    with col_freq:
        st.markdown("**Personalizzazione POS 003**")
        freq_pest = st.selectbox("Frequenza Controlli Pest", 
                                ["Quadrimestrale", "Bimestrale", "Mensile", "Trimestrale"])

    st.markdown("---")
    st.subheader("Caricamento Allegato Variabile")
    st.markdown("Carica la **Planimetria Trappole** specifica per questo cliente.")
    uploaded_planimetria = st.file_uploader("Trascina file (JPG/PNG)", type=["jpg", "png", "jpeg"])

    submit_btn = st.form_submit_button("GENERA MANUALE PDF COMPLETO", type="primary")

# --- LOGICA GENERAZIONE PDF ---
if submit_btn:
    if not ragione_sociale:
        st.error("Inserire almeno la Ragione Sociale.")
    else:
        # 1. Setup PDF
        pdf = PDF(client_name=ragione_sociale, reason_social=ragione_sociale)
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # --- COPERTINA (Stile Relazione) ---
        pdf.ln(40)
        pdf.set_font("Helvetica", "B", 24)
        pdf.multi_cell(0, 10, "MANUALE DI CORRETTA PRASSI\nPER BENESSERE E BIOSICUREZZA", align="C")
        pdf.ln(10)
        
        # Immagine Copertina
        if os.path.exists("assets/cover.jpg"):
            x_centered = (pdf.w - 140) / 2
            pdf.image("assets/cover.jpg", x=x_centered, w=140)
        
        pdf.ln(20)
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "Azienda:", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Helvetica", "", 16)
        pdf.cell(0, 10, ragione_sociale, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Helvetica", "", 12)
        pdf.cell(0, 10, f"Codice Stalla: {codice_stalla}", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # --- PAGINA 1: ANAGRAFICA ---
        pdf.add_page()
        pdf.section_title("SCHEDA ANAGRAFICA E RESPONSABILITÀ")
        
        # Tabella Anagrafica personalizzata
        with pdf.table(col_widths=(40, 100), text_align="L") as table:
            data_rows = [
                ("Ragione Sociale", ragione_sociale),
                ("Indirizzo Sede", indirizzo),
                ("Partita IVA", piva),
                ("Codice Stalla", codice_stalla),
                ("Resp. Biosicurezza", resp_bio),
                ("Resp. Benessere", resp_ben),
                ("Data Corso Ben.", data_corso.strftime("%d/%m/%Y")),
            ]
            for label, value in data_rows:
                row = table.row()
                row.cell(label, style=FontFace(emphasis="BOLD"))
                row.cell(value)

        # --- POS 001 ---
        pdf.add_page()
        pdf.section_title("POS 001 - GESTIONE VISITATORI")
        pdf.paragraph(TXT_POS_001)

        # --- POS 002 ---
        pdf.add_page()
        pdf.section_title("POS 002 - GESTIONE QUARANTENA")
        pdf.paragraph(TXT_POS_002)

        # --- POS 003 (DINAMICO) ---
        pdf.add_page()
        pdf.section_title("POS 003 - PEST MANAGEMENT")
        # Inserimento variabile frequenza (minuscolo per scorrere nel testo)
        txt_pos3_filled = TXT_POS_003_TEMPLATE.format(frequenza=freq_pest.lower())
        pdf.paragraph(txt_pos3_filled)

        # --- POS 004 ---
        pdf.add_page()
        pdf.section_title("POS 004 - BENESSERE ANIMALE")
        pdf.paragraph(TXT_POS_004)

        # --- ALLEGATI ---
        pdf.add_page()
        pdf.section_title("ALLEGATI OBBLIGATORI")
        pdf.paragraph("Di seguito sono riportati i documenti e la cartellonistica citati nelle Procedure Operative Standard.")

        # ALLEGATO 1: CARTELLO
        pdf.add_page()
        pdf.sub_title("ALLEGATO 1: CARTELLO BIOSICUREZZA (INGRESSO)")
        if os.path.exists("assets/cartello.jpg"):
            pdf.image("assets/cartello.jpg", w=170, x=20, y=50)
        else:
            pdf.paragraph("[ERRORE: Immagine cartello.jpg non trovata]")

        # ALLEGATO 2: PLANIMETRIA (VARIABILE)
        pdf.add_page()
        pdf.sub_title("ALLEGATO 2: PLANIMETRIA PEST CONTROL")
        if uploaded_planimetria:
            temp_path = "temp_plan.jpg"
            with open(temp_path, "wb") as f:
                f.write(uploaded_planimetria.getbuffer())
            pdf.image(temp_path, w=170, x=20, y=50)
        else:
            pdf.paragraph("[NESSUNA PLANIMETRIA CARICATA IN FASE DI INPUT]")
            # Box vuoto come placeholder
            pdf.rect(20, 50, 170, 100)
            pdf.text(80, 100, "Spazio per Planimetria")

        # ALLEGATO 3: BCS
        pdf.add_page()
        pdf.sub_title("ALLEGATO 3: INFOGRAFICA BCS")
        if os.path.exists("assets/bcs.jpg"):
            pdf.image("assets/bcs.jpg", w=170, x=20, y=50)

        # ALLEGATO 4: CHECKLIST (NUOVO RICHIESTO)
        pdf.add_page()
        pdf.section_title("CHECK LIST DI MONITORAGGIO PERIODICO")
        pdf.paragraph("La seguente lista di controllo deve essere utilizzata dal Responsabile Biosicurezza con cadenza mensile per verificare il mantenimento dei requisiti.")
        
        pdf.ln(5)
        # Rendering Tabella Checklist
        with pdf.table(col_widths=(30, 100, 30), text_align="L") as table:
            # Header
            header = table.row()
            for h in CHECKLIST_DATA[0]:
                header.cell(h, style=FontFace(emphasis="BOLD", fill_color=(230, 230, 230)))
            
            # Rows
            for row_data in CHECKLIST_DATA[1:]:
                r = table.row()
                r.cell(row_data[0])
                r.cell(row_data[1])
                r.cell(row_data[2]) # Cella vuota per la spunta

        # --- OUTPUT FILE ---
        temp_file = "Manuale_Finale.pdf"
        pdf.output(temp_file)
        
        with open(temp_file, "rb") as f:
            pdf_data = f.read()
            
        st.success("✅ Manuale Generato Correttamente!")
        st.download_button("📥 SCARICA PDF FINALE", data=pdf_data, file_name=f"Manuale_{ragione_sociale}.pdf", mime="application/pdf")
