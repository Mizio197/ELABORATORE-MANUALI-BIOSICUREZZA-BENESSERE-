import streamlit as st
from fpdf import FPDF
import datetime
import os
from PIL import Image
import tempfile

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="R-ADVISOR Generator", page_icon="📄", layout="centered")

# --- 1. FUNZIONE PULIZIA TESTO (Preventiva per caratteri Word) ---
def clean_text(text):
    if text is None: return ""
    text = str(text)
    
    # Mappa manuale dei caratteri Word più comuni che creano problemi
    replacements = {
        u'\u2018': "'", u'\u2019': "'", u'\u201c': '"', u'\u201d': '"',
        u'\u2013': '-', u'\u2014': '-', u'\u2026': '...', 
        u'\u00B0': ' gradi ', u'\u20ac': 'EUR', 
        u'’': "'", u'“': '"', u'”': '"', u'–': '-'
    }
    for key, value in replacements.items():
        text = text.replace(key, value)
    
    # Forza la codifica Latin-1: se trova un carattere impossibile (es. emoji), mette un '?'
    # Questo impedisce il crash del PDF
    return text.encode('latin-1', 'replace').decode('latin-1')

# --- 2. FUNZIONE IMMAGINE SICURA (Anti-Crash per Loghi e Foto) ---
def get_safe_image_path(original_path):
    # Se il file non esiste, ritorna None
    if not os.path.exists(original_path):
        return None
    
    try:
        img = Image.open(original_path)
        
        # Converte tutto in RGB (rimuove trasparenze che fanno crashare i PDF)
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.convert('RGBA').split()[-1])
            img = bg
        else:
            img = img.convert('RGB')
        
        # Salva in un file temporaneo .jpg
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            img.save(tmp, format='JPEG', quality=90)
            return tmp.name
    except Exception as e:
        # Se l'immagine è corrotta, la ignora invece di bloccare tutto
        return None

# --- 3. CLASSE PDF ---
class PDF(FPDF):
    def __init__(self, client_name):
        super().__init__()
        self.client_name = clean_text(client_name)

    def header(self):
        # Carica il logo in modo sicuro
        safe_logo = get_safe_image_path("assets/logo.png")
        if safe_logo:
            try:
                self.image(safe_logo, x=160, y=10, w=40)
            except: pass
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        text = f"ELABORATO CON R-ADVISOR-APP da STUDIO SUMMIT SRL per {self.client_name} - Pagina {self.page_no()}/{{nb}}"
        self.cell(0, 10, clean_text(text), align="C")

    def chapter_title(self, label):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, clean_text(label), ln=True, align='L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font("Helvetica", "", 11)
        self.multi_cell(0, 6, clean_text(body), align='J') 
        self.ln()

# --- 4. TESTI INTEGRALI (POS) ---

POS_001_TEXT = """Scopo: Prevenire l'introduzione e la diffusione di agenti patogeni (virus, batteri, parassiti) all'interno dell'unita' epidemiologica tramite vettori meccanici (veicoli, persone, attrezzature).
Riferimenti Normativi: Reg. UE 2016/429; Liste di controllo ClassyFarm/SNQBA.

1. Classificazione del Rischio Visitatori
Nelle more dell'analisi del rischio condotta per garantire una migliore efficacia delle attivita' di gestione ai fini della biosicurezza, si e' provveduto a classificare in categorie gli stessi in differenti categorie:

Categoria A: Visitatori ad Alto Rischio (Professionali)
Soggetti che, per la natura della loro attivita', frequentano regolarmente piu' allevamenti o hanno contatti diretti con animali.
Chi sono: Medici Veterinari, tecnici fecondatori, trasportatori di animali vivi, trasportatori di mangime (se entrano in zona pulita), tecnici manutentori di impianti zootecnici, pareggiatori, tosapecore, consulenti nutrizionisti.
Requisito specifico: Devono dichiarare preliminarmente all'accesso eventuali contatto con animali infetti, animali di nuova introduzione in altri allevamenti e, piu' in generale, altri fattori di rischio, anche solo potenziale. Onere dell'operatore e' la valutazione specifica di ogni singola dichiarazione di rischio.

Categoria B: Visitatori a Medio/Basso Rischio
Soggetti che non hanno contatti frequenti con altri allevamenti o che non accederanno alle zone di stabulazione diretta.
Chi sono: Fornitori di servizi vari (elettricisti, idraulici non specializzati in zootecnia), rappresentanti commerciali, visitatori istituzionali, scolaresche (se ammesse).

2. Procedura di Accesso (Zona Filtro)
L'accesso all'allevamento e' consentito esclusivamente attraverso l'unico varco d'ingresso identificato e segnalato.
Tutti i visitatori, indipendentemente dalla categoria, devono attenersi alla seguente procedura:
a) Arrivo e Parcheggio: Lasciare il proprio automezzo nell'area di parcheggio esterna ("Zona Sporca"), salvo specifica autorizzazione per carico/scarico materiali pesanti (in tal caso il mezzo dovra' essere disinfettato alle ruote e passaruota).
b) Registrazione: Compilare il "Registro Visitatori" indicando:
- Nome e Cognome.
- Azienda/Ente di appartenenza.
- Targa del veicolo (se entrato).
- Dichiarazione circa condizioni di potenziale rischio Luogo e data dell'ultimo contatto con animali da reddito (essenziale per Categoria A).

3. Dispositivi di Protezione (DPI)
Prima di accedere alla "Zona Pulita" (area di allevamento), il visitatore deve indossare i DPI forniti dall'azienda o i propri se giudicati idonei e puliti dal Responsabile Biosicurezza.
Dotazione Minima:
- Calzari monouso o stivali aziendali dedicati.
- Camice monouso o tuta da lavoro pulita.
- Cuffia copricapo (se necessaria).

4. Comportamento all'interno dell'Allevamento
Accompagnamento: I visitatori non possono mai muoversi liberamente in azienda. Devono essere costantemente accompagnati dal titolare o da un delegato.
Percorsi: Rispettare rigorosamente il flusso "Marcia in Avanti" (dal pulito allo sporco / dagli animali piu' giovani ai piu' anziani), salvo diversa indicazione veterinaria.
Divieti:
- Vietato toccare gli animali se non strettamente necessario e autorizzato.
- Vietato introdurre cibo o bevande nelle aree di stabulazione.
- Vietato introdurre attrezzature personali (cellulari, tablet) se non protette o precedentemente disinfettate con salviette imbevute.

5. Cartellonistica
All'ingresso della proprieta' (cancello principale) e all'ingresso della zona filtro, e' stato predisposto ed affisso in modo ben visibile il seguente cartello:
ATTENZIONE - ZONA A BIOSICUREZZA CONTROLLATA
E' SEVERAMENTE VIETATO L'INGRESSO AI NON AUTORIZZATI
Per accedere a questa struttura e' OBBLIGATORIO:
- Annunciare la propria presenza e attendere il personale.
- Non entrare senza autorizzazione.
- Registrare il proprio ingresso nell'apposito modulo.
- Indossare i DPI forniti dall'azienda (calzari, camice, cuffia).
- Sottoporre gli automezzi autorizzati a disinfezione."""

POS_002_TEXT = """Scopo: Definire le modalita' operative per l'introduzione di nuovi capi (acclimatamento e controllo sanitario) e per la gestione di animali residenti che manifestano segni clinici di malattia infettiva, al fine di garantire la compartimentazione sanitaria.
Riferimenti: Reg. UE 2016/429 (Animal Health Law); Manuale ClassyFarm (Area C - Biosicurezza); Disciplinare SNQBA.

1. Definizione e Requisiti delle Aree
L'azienda identifica due aree funzionali distinte:

1.1 Box di Quarantena (Nuovi Arrivi)
Ubicazione: Risulta fisicamente separata dai gruppi di produzione (stalla vacche in lattazione, box vitelli sani).
Caratteristiche:
- Mangiatoia e abbeveratoio dedicati e non condivisi con box limitrofi.
- Pavimentazione facilmente lavabile e disinfettabile.

1.2 Box Infermeria/Isolamento (Animali Malati)
Si tratta di area dedicata a capi residenti (adulti o vitelli) che manifestano patologie (es. mastiti contagiose, zoppie gravi infette, sindromi respiratorie, diarree neonatali). Garantisce il benessere dell'animale malato (lettiera pulita, asciutta, spazio adeguato, facile accesso all'acqua).

2. Procedura per Nuovi Ingressi (Quarantena)
Questa procedura si applica a qualsiasi animale proveniente dall'esterno, prescindendo dall'eta'.
2.1 Fase Pre-Ingresso
Si provvede a verifica dello stato sanitario dell'allevamento di provenienza (tramite Modello 4 e attestazioni sanitarie).

2.2 Gestione Periodo di Quarantena
Durata: Minimo 21 giorni (o diverso periodo indicato dal Veterinario Aziendale).
Attivita':
- Isolamento completo dal resto della mandria.
- Osservazione quotidiana per rilevare segni clinici.
- Esecuzione dei prelievi ematici/tamponi previsti dai piani di risanamento o concordati con il Veterinario.
- Utilizzo di attrezzature dedicate (pale, forche) o accurata disinfezione dopo l'uso nel box quarantena.

3. Procedura per Animali Malati (Isolamento)
Identificazione: L'animale sospetto viene immediatamente identificato e spostato nel Box Infermeria.
Gestione:
- L'animale viene munto per ultimo (se in lattazione) con gruppo di mungitura separato o sanificato dopo l'uso.
- Le cure vengono prestate dopo aver accudito gli animali sani (flusso "dai sani ai malati").

4. Pulizia e Vuoto Sanitario
4.1 Pulizia Box
Ogni volta che un animale (o un gruppo omogeneo) in quarantena/isolamento viene spostato in stalla o esce (guarigione/macellazione), il box e' sottoposto alle seguenti attivita':
- Svuotato completamente dalla lettiera.
- Lavato con idropulitrice (acqua calda se possibile) per rimuovere il biofilm.
- Disinfettato con prodotto virucida/battericida approvato.
- Lasciato asciugare (vuoto sanitario) prima di introdurre un nuovo animale.

4.2 Gestione Letame
La lettiera rimossa dall'area quarantena/isolamento NON viene distribuita direttamente sui campi o mischiata subito al letame "maturo".
Tale lettiera viene stoccata in un punto dedicato della concimaia per subire un processo di biotermizzazione (compostaggio naturale che raggiunge >60 gradi C) per inattivare virus e batteri prima dello spandimento agronomico.

5. Registrazione e Tracciabilita'
Per ogni animale in Quarantena/Isolamento si provvede a compilare la Scheda di Stalla/Cartella Clinica contenente:
- ID Animale.
- Data ingresso in isolamento e motivo.
- Trattamenti farmacologici effettuati (data, farmaco, quantita', tempi di sospensione) - Rif. Registro Trattamenti Elettronico.
- Esiti esami di laboratorio.
- Data di fine isolamento/esito (guarigione, macellazione, decesso)."""

POS_004_TEXT = """Scopo: Descrivere le modalita' operative adottate dall'azienda per garantire il rispetto dei fabbisogni fisiologici ed etologici dei bovini in tutte le fasi di allevamento (vitelli, manze, vacche in lattazione e asciutta), in conformita' alla normativa vigente e ai requisiti del Sistema di Qualita' Nazionale per il Benessere Animale (SNQBA).
Riferimenti: D.Lgs 146/2001; D.Lgs 126/2011; Manuale ClassyFarm (Area A - Management e Personale, Area B - Strutture).

1. Formazione e Competenza del Personale
La gestione degli animali e' affidata esclusivamente a personale qualificato.
Si provvede affinche' tutti gli operatori ricevano una formazione adeguata, sia mediante partecipazione a corsi che mediante affiancamento con il Veterinario Aziendale, sulle corrette modalita' di manipolazione, sul riconoscimento dei segni di malattia e sui principi di biosicurezza.
E' garantita l'ispezione di tutti gli animali presenti in allevamento almeno due volte al giorno (mattina e sera). Qualora si riscontrino animali feriti o con segni di sofferenza, si procede all'immediato isolamento e trattamento secondo i protocolli sanitari concordati con il Veterinario.

2. Gestione della Vitellaia (0-6 Mesi)
2.1 Colostratura e Alimentazione
Si provvede alla somministrazione di colostro di alta qualita' (verificato con rifrattometro Brix >22%) entro le prime 6 ore di vita, in quantita' pari al 10% del peso vivo (circa 3-4 litri).
L'acqua e' sempre a disposizione, pulita e fresca, fin dalla prima settimana di vita.
2.2 Alloggiamento
I vitelli sono stabulati in box singoli (nel rispetto delle dimensioni di legge) fino a massimo 8 settimane di vita. Le pareti dei box sono forate per consentire il contatto visivo e tattile con i consimili (benessere sociale). Dopo le 8 settimane, i vitelli vengono spostati in box multipli.

3. Pratiche Zootecniche e Mutilazioni
In conformita' ai requisiti SNQBA, si attuano procedure per minimizzare il dolore.
Decornazione: Si provvede alla decornazione dei vitelli entro la 3a-4a settimana di vita (bottone corneo mobile). L'intervento viene effettuato mediante cauterizzazione termica, previo utilizzo di anestesia locale (blocco del nervo cornuale) e somministrazione di analgesico/antinfiammatorio sistemico (FANS) per la gestione del dolore post-operatorio.
Code: E' vietato il taglio della coda (caudectomia).
Movimentazione: E' vietato l'uso di pungoli elettrici, bastoni o calci per spostare gli animali. Si utilizzano pannelli di spinta o movimenti corporei che sfruttano il comportamento naturale della mandria.

4. Monitoraggio Indicatori Animal-Based
Si provvede al monitoraggio periodico (es. trimestrale o semestrale tramite ClassyFarm) dei seguenti indicatori di benessere direttamente sugli animali:
- Body Condition Score (BCS): Per valutare lo stato nutrizionale.
- Locomotion Score: Per rilevare precocemente zoppie.
- Cleanliness Score: Per valutare l'igiene degli animali (mammella e arti).
- Lesioni: Verifica assenza di lesioni cutanee, al garretto o al collo (indicatori di strutture inadeguate).

5. Gestione delle Emergenze
L'azienda e' dotata di gruppo elettrogeno a riarmo automatico per garantire il funzionamento degli impianti di mungitura, abbeverata e ventilazione anche in caso di blackout elettrico.
E' presente un sistema di allarme (SMS/telefonico) che segnala tempestivamente guasti critici."""

# --- 5. INTERFACCIA UTENTE ---
st.title("R-ADVISOR-APP | Generatore Manuali")
st.success("Sistema Caricato. Compila i dati.")

with st.form("data_entry_form"):
    st.subheader("1. Anagrafica Azienda")
    col1, col2 = st.columns(2)
    with col1:
        ragione_sociale = st.text_input("Ragione Sociale / Nome Cliente")
        indirizzo = st.text_input("Indirizzo Sede Operativa")
        codice_stalla = st.text_input("Codice Stalla (ASL)")
        telefono = st.text_input("Recapito Telefonico")
    with col2:
        email = st.text_input("Email")
        veterinario = st.text_input("Veterinario Aziendale (Nome Cognome)")
        resp_biosicurezza = st.text_input("Responsabile Biosicurezza")
        resp_benessere = st.text_input("Responsabile Benessere")
        data_attestato = st.date_input("Data Rilascio Attestato Benessere", datetime.date.today())

    st.subheader("2. Personalizzazioni POS")
    freq_pest_control = st.selectbox(
        "Frequenza monitoraggio Pest Control (Ditta Esterna)", 
        ["Quadrimestrale", "Bimestrale", "Mensile", "Semestrale"], index=0
    )

    st.subheader("3. Allegati Specifici Cliente")
    planimetria_file = st.file_uploader("Carica Planimetria Pest Control (Immagine JPG/PNG)", type=['png', 'jpg', 'jpeg'])

    submitted = st.form_submit_button("GENERA MANUALE PDF")

# --- 6. LOGICA GENERAZIONE ---
if submitted:
    if not ragione_sociale:
        st.error("Inserire almeno la Ragione Sociale per procedere.")
    else:
        # Costruzione POS 003 DINAMICO
        pos_003_text = f"""Scopo: Descrivere le misure di difesa passiva (Pest Proofing) e attiva (Pest Control) messe in atto dall'azienda per controllare la presenza di roditori, insetti e altri animali indesiderati, vettori di patologie e minaccia per la salubrita' dei mangimi e il benessere animale.
Riferimenti: Reg. (UE) 852/2004; Reg. (UE) 2016/429; SNQBA / ClassyFarm (Area Biosicurezza).

1. Responsabilita' e Gestione del Servizio
La gestione del piano di lotta agli infestanti e' suddivisa tra il personale interno e una ditta specializzata esterna.
Responsabile Biosicurezza (Interno): Sovrintende alla corretta applicazione delle misure di difesa passiva, segnala tempestivamente anomalie e archivia la documentazione.
Ditta Specializzata (Esterno): Il servizio di monitoraggio e lotta attiva e' affidato alla ditta STUDIO SUMMIT SRL (Iscritta ANID - Associazione Nazionale Imprese Disinfestazione). La ditta possiede i requisiti tecnico-professionali per la gestione dei presidi e l'uso di biocidi conformi alla normativa vigente.

2. Pest Proofing (Difesa Passiva e Prevenzione)
L'azienda attua sistematicamente misure strutturali e comportamentali volte a impedire l'ingresso e la nidificazione degli infestanti (esclusione). Nello specifico:

2.1 Gestione Edifici e Strutture
- Si mantengono integre le reti anti-passero e anti-insetto alle finestre.
- Si verifica la tenuta delle porte e dei portoni (assenza di fessure inferiori > 5mm).
- Si sigillano fori di passaggio tubature/cavi nelle murature.

2.2 Gestione Ambientale Esterna
- La vegetazione perimetrale e' mantenuta rasata per non offrire rifugio ai roditori.
- Si evita l'accumulo di materiali di scarto, rottami o rifiuti a ridosso delle pareti esterne delle stalle.
- La zona di stoccaggio mangimi e' mantenuta pulita da spandimenti accidentali.

3. Pest Control (Lotta Attiva e Monitoraggio)
Il piano di monitoraggio prevede l'installazione di postazioni fisse (erogatori di sicurezza) numerate e riportate in planimetria.
Tipologia Postazioni:
- Interno Stalle/Sale Latte: Trappole a cattura (meccaniche o collanti) o virtuali (monitoraggio tracce) senza uso di veleni, per evitare contaminazioni.
- Esterno Perimetrale: Erogatori per esche rodenticide (in blocchi paraffinati fissati all'asta di sicurezza) conformi alla normativa Biocidi.

Frequenza Interventi: Il monitoraggio viene effettuato da STUDIO SUMMIT SRL con cadenza {freq_pest_control.upper()}.
In ogni caso, il numero di passaggi vengono modulati dalla ditta fornitrice in relazione al livello di infestazione effettivamente riscontrato durante i monitoraggi (soglia di tolleranza).

4. Gestione Documentale e Planimetria
Tutta l'attivita' di Pest Management e' tracciata e documentata per garantire la rintracciabilita' delle operazioni.
Planimetria Dispositivi: E' presente e aggiornata una mappa planimetrica dell'azienda (Allegato PM-01) che identifica univocamente la posizione di ogni erogatore (numerati progressivamente).
Report di Intervento: Al termine di ogni visita, STUDIO SUMMIT SRL rilascia un rapporto di intervento che riporta:
- Data e ora dell'intervento.
- Prodotti utilizzati (nome commerciale, principio attivo, n. registrazione, lotto).
- Esito del monitoraggio per ogni singola postazione (es. consumo: nullo, parziale, totale).
- Eventuali "Non Conformita'" rilevate o azioni correttive suggerite.
Schede Tecniche e di Sicurezza: Sono archiviate e disponibili le SDS (Schede di Sicurezza) aggiornate di tutti i formulati chimici impiegati in azienda.

5. Procedura di Emergenza (Avvistamento Interno)
Qualora il personale aziendale rilevi la presenza di infestanti (roditori o insetti in massa) tra un controllo programmato e l'altro:
- L'operatore segnala l'evento al Responsabile Biosicurezza.
- Il Responsabile contatta immediatamente STUDIO SUMMIT SRL.
- Viene attivato un intervento straordinario di verifica e trattamento entro i tempi concordati contrattualmente."""

        try:
            pdf = PDF(ragione_sociale)
            pdf.alias_nb_pages()
            pdf.set_auto_page_break(auto=True, margin=15)

            # 1. COPERTINA
            pdf.add_page()
            safe_cover = get_safe_image_path("assets/cover.jpg")
            if safe_cover:
                pdf.image(safe_cover, x=35, y=40, w=140)
            
            pdf.set_y(150)
            pdf.set_font("Helvetica", "B", 24)
            pdf.cell(0, 15, clean_text("MANUALE DI CORRETTA PRASSI"), ln=True, align='C')
            pdf.cell(0, 15, clean_text("PER BENESSERE E BIOSICUREZZA"), ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Helvetica", "", 18)
            pdf.cell(0, 15, clean_text(ragione_sociale), ln=True, align='C')
            
            # 2. ANAGRAFICA
            pdf.add_page()
            pdf.chapter_title("SCHEDA ANAGRAFICA AZIENDALE")
            pdf.set_font("Helvetica", "", 12)
            
            def add_row(label, value):
                pdf.set_font("Helvetica", "B", 11)
                pdf.cell(80, 10, clean_text(label), border=1)
                pdf.set_font("Helvetica", "", 11)
                pdf.cell(0, 10, clean_text(str(value)), border=1, ln=True)

            add_row("Ragione Sociale", ragione_sociale)
            add_row("Indirizzo", indirizzo)
            add_row("Codice Stalla", codice_stalla)
            add_row("Telefono", telefono)
            add_row("Email", email)
            add_row("Veterinario Aziendale", veterinario)
            add_row("Resp. Biosicurezza", resp_biosicurezza)
            add_row("Resp. Benessere", resp_benessere)
            add_row("Data Attestato Benessere", data_attestato.strftime("%d/%m/%Y"))

            # 3. SEZIONI POS
            pdf.add_page()
            pdf.chapter_title("POS-BIO-01: GESTIONE E REGOLE VISITATORI ESTERNI")
            pdf.chapter_body(POS_001_TEXT)
            
            pdf.add_page()
            pdf.chapter_title("POS-BIO-02: GESTIONE E REGOLE QUARANTENA")
            pdf.chapter_body(POS_002_TEXT)
            
            pdf.add_page()
            pdf.chapter_title("POS-BIO-03: GESTIONE E REGOLE PEST MANAGEMENT")
            pdf.chapter_body(pos_003_text)
            
            pdf.add_page()
            pdf.chapter_title("POS-BIO-04: GESTIONE E REGOLE BENESSERE ANIMALE")
            pdf.chapter_body(POS_004_TEXT)

            # 4. ALLEGATI
            pdf.add_page()
            pdf.chapter_title("SEZIONE ALLEGATI")
            
            pdf.ln(5)
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 10, "ALLEGATO 1: CARTELLONISTICA VISITATORI", ln=True)
            
            safe_cartello = get_safe_image_path("assets/cartello.jpg")
            if safe_cartello:
                pdf.image(safe_cartello, x=30, w=150)
            else:
                pdf.set_font("Helvetica", "I", 10)
                pdf.cell(0, 10, "Immagine cartello non trovata (controlla nome file)", ln=True)
            
            pdf.add_page()
            pdf.cell(0, 10, "ALLEGATO 2: PLANIMETRIA PEST CONTROL", ln=True)
            if planimetria_file is not None:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_up:
                    tmp_up.write(planimetria_file.read())
                    tmp_up_path = tmp_up.name
                safe_plan = get_safe_image_path(tmp_up_path)
                if safe_plan:
                    pdf.image(safe_plan, x=20, w=170)
                try: os.remove(tmp_up_path)
                except: pass
            else:
                pdf.set_font("Helvetica", "I", 10)
                pdf.cell(0, 10, "Nessuna planimetria caricata.", ln=True)

            pdf.add_page()
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 10, "ALLEGATO 3: INFOGRAFICA BODY CONDITION SCORE (BCS)", ln=True)
            
            safe_bcs = get_safe_image_path("assets/bcs.jpg")
            if safe_bcs:
                pdf.image(safe_bcs, x=20, w=170)
            else:
                pdf.set_font("Helvetica", "I", 10)
                pdf.cell(0, 10, "Immagine BCS non trovata", ln=True)

            # --- GENERAZIONE OUTPUT DEFINITIVA ---
            # CORREZIONE: output() restituisce già bytearray, NON bisogna fare .encode()
            pdf_content = pdf.output()
            
            st.success("Manuale generato con successo!")
            filename = f"Manuale_Biosicurezza_{ragione_sociale.replace(' ', '_')}.pdf"
            st.download_button(
                label="SCARICA IL MANUALE PDF",
                data=pdf_content,
                file_name=filename,
                mime="application/pdf"
            )
            
        except Exception as e:
            st.error(f"Errore tecnico: {e}")
