# 5. Dati, RAG e conoscenza

## 5.1 La qualita nasce dai dati

Un sistema AI non migliora solo scegliendo un modello piu grande. Dati incompleti, duplicati, obsoleti o privi di contesto producono risposte fragili anche con un modello capace.

Prima dell'indicizzazione occorre conoscere:

- origine e proprietario del dato;
- data e versione;
- formato e struttura;
- livello di affidabilita;
- permessi di accesso;
- frequenza di aggiornamento;
- eventuali dati personali o riservati.

## 5.2 Dal documento al blocco di conoscenza

Un documento non va trattato come una stringa da tagliare a intervalli fissi. Il significato puo dipendere da titolo, sezione, tabella, definizione, nota, data o relazione con altre parti.

Un blocco utile dovrebbe essere:

- abbastanza completo da rispondere a una domanda;
- abbastanza piccolo da essere recuperato con precisione;
- collegato alla sezione e al documento di origine;
- accompagnato da versione, stato e metadati;
- separato da contenuti incompatibili o superati.

La segmentazione automatica e un punto di partenza. I documenti complessi richiedono controllo della struttura e, quando serve, navigazione tra blocchi collegati.

## 5.3 RAG non significa verita automatica

Il retrieval augmented generation recupera fonti esterne e le inserisce nel contesto del modello. Questo riduce la probabilita di inventare informazioni, ma restano possibili errori di estrazione, ricerca, selezione e sintesi.

Una pipeline deve quindi valutare separatamente:

1. recall: la fonte corretta viene recuperata?
2. precision: i risultati sono pertinenti?
3. grounding: la risposta deriva davvero dalle fonti?
4. citation: il lettore puo verificare l'affermazione?
5. access control: il sistema evita fonti non autorizzate?

## 5.4 Ricerca ibrida

La ricerca lessicale e necessaria per acronimi, codici, standard e nomi esatti. La ricerca semantica aiuta quando la domanda usa parole diverse da quelle del documento.

Una ricerca robusta combina:

- indice testuale;
- embeddings;
- filtri sui metadati;
- reranking;
- espansione verso concetti collegati;
- citazioni e contesto circostante.

Nessun singolo punteggio deve decidere da solo la risposta in domini ad alto rischio.

## 5.5 Quando il RAG non basta

Il RAG fornisce conoscenza dichiarativa. Non sostituisce automaticamente procedure, autorizzazioni, regole o memoria operativa.

Usare una skill per una procedura, regole deterministiche per un vincolo, MCP per collegarsi a un sistema e RAG per recuperare documentazione. La qualita nasce dalla composizione corretta, non dal mettere tutto nello stesso prompt.

## Fonti di partenza

- `Why RAG Solutions Fail with Complex Documents & Vector Databases`
- `What Is Chunkless RAG How Docling & AI Agents Navigate Documents`
- `AI & Data Science Periodic Tables How They Work Together`
- `Essential Skills for Becoming an AI Engineer RAG, AI Agents, & More`
- `Is Fine-Tuning Still Needed LLMs, RAG, & LoRA`
- `What Is a Digital Librarian AI Agent Connecting SQL & Vector Database`
