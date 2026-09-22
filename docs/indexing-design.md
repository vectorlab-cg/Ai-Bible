# Ricerca e indicizzazione

## Obiettivo

La versione finale della Bibbia sara un corpus unico di documenti editoriali, interrogabile con ricerca testuale e semantica. La ricerca dovra restituire contenuto leggibile, riferimenti e contesto, non solo frammenti simili.

## Unita dell'indice

L'unita principale sara il `knowledge_block`, derivato dai capitoli approvati:

- `id` stabile;
- `chapter_id` e titolo del capitolo;
- `section_id` e titolo della sezione;
- testo autosufficiente;
- tipo: `definition`, `principle`, `procedure`, `comparison`, `risk`, `example` o `case-study`;
- concetti collegati;
- livello di maturita: `draft`, `reviewed`, `approved`;
- validita temporale;
- fonti e note di provenienza.

Un blocco non deve dipendere da una frase presente in un altro blocco per essere comprensibile nei risultati della ricerca.

## Strategia di ricerca

La prima versione usera ricerca ibrida:

1. ricerca lessicale per termini esatti, acronimi, nomi di standard e tecnologie;
2. ricerca semantica per domande formulate con parole diverse dal testo;
3. fusione e reranking dei risultati;
4. filtri per capitolo, concetto, tipo, stato e validita;
5. espansione tramite concetti correlati;
6. citazioni al blocco e alla fonte di origine.

La ricerca semantica non sostituisce quella lessicale: `ISO 42001`, `MCP`, `RAG` e nomi di prodotti richiedono corrispondenza precisa.

## Metadati minimi

```json
{
  "id": "kb-0001",
  "chapter_id": "fondamenti",
  "section_id": "rag-grounding",
  "title": "RAG e grounding",
  "type": "principle",
  "concepts": ["rag", "hallucinations"],
  "status": "reviewed",
  "temporal_scope": "stable",
  "source_ids": ["source-id"],
  "source_spans": [
    {"source_id": "source-id", "start_time": "00:01:00,000", "end_time": "00:03:00,000"}
  ],
  "text": "..."
}
```

L'indice locale deriva i riferimenti `source_id` dai titoli elencati nelle sezioni "Fonti di partenza" dei capitoli. Il riferimento e di livello fonte, non ancora di livello timestamp: i blocchi senza un matching univoco restano marcati per revisione.

## Citazioni e provenienza

La Bibbia non conservera le trascrizioni originali nella distribuzione finale, ma ogni blocco approvato manterra una provenienza compatta:

- titolo della fonte;
- `source_id` e hash;
- intervallo temporale, quando disponibile;
- stato della verifica;
- eventuale nota che segnala una notizia datata o un'affermazione da confermare.

Questo consente di verificare il contenuto durante la revisione senza trasformare l'indice in una copia del corpus grezzo.

## Fasi di implementazione

1. approvare i capitoli editoriali;
2. suddividere i capitoli in blocchi autosufficienti;
3. validare schema e metadati;
4. generare indice lessicale;
5. aggiungere embeddings e indice semantico;
6. costruire il retriever ibrido;
7. creare un set di domande di valutazione;
8. misurare precisione, copertura, citazioni e latenza;
9. eliminare le fonti temporanee solo dopo la verifica finale.

La prima implementazione locale e disponibile con:

```powershell
python tools\build_bible_index.py docs\bible docs\bible-index.json
python tools\build_bible_index.py docs\bible docs\bible-index.json --inventory docs\corpus-inventory.json
python tools\search_bible.py docs\bible-index.json "RAG grounding"
```

L'indice lessicale contiene 123 blocchi derivati dai sette capitoli attuali. 112 blocchi hanno 670 riferimenti validi all'inventario delle fonti; 11 blocchi del capitolo temporale richiedono ancora un matching editoriale piu preciso. E un indice di lavoro: prima di aggiungere embeddings bisogna approvare i blocchi, completare la provenienza e creare domande di valutazione rappresentative.

## Criterio di successo

Una domanda di prova deve restituire:

- una risposta fondata su uno o piu blocchi approvati;
- citazioni verificabili;
- nessun blocco ormai superato quando esiste una versione piu recente;
- un'indicazione esplicita quando la Bibbia non contiene la risposta.

Prima verra realizzato un indice locale semplice e riproducibile. La scelta di un vector database verra fatta solo dopo aver misurato il corpus e la qualita della ricerca.
