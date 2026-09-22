# Revisione della copertura

## Stato attuale

La matrice `docs/source-coverage.json` collega le fonti ai segmenti di lavorazione e ai candidati concettuali.

- fonti presenti: `65`;
- fonti con almeno un segmento: `65`;
- segmenti totali: `383`;
- segmenti con almeno un candidato concettuale: `383`;
- segmenti ancora da classificare: `0`;

## Interpretazione

La presenza di una fonte nella matrice non significa che tutto il suo contenuto sia entrato nella Bibbia. Significa solo che la fonte e stata segmentata e che almeno un suo segmento e stato collegato al processo di estrazione.

La Bibbia sara completa solo quando ogni segmento utile avra uno di questi esiti:

- incorporato in un blocco editoriale approvato;
- registrato come duplicato;
- registrato come contenuto temporale;
- escluso con una motivazione editoriale;
- marcato per revisione manuale.

La provenienza dei blocchi editoriali e ora presente nell'indice locale a livello di fonte: 112 blocchi hanno 670 riferimenti validi. Questo non equivale ancora a citazioni puntuali con timestamp.

La classificazione concettuale copre tutti i 383 segmenti. Un segmento di chiusura video e marcato come esclusione editoriale, quindi copertura completa non significa che ogni frase verra pubblicata nella Bibbia.

Un primo mapping automatico ha trovato 144 intervalli timestamp candidati per 52 blocchi. Lo stato resta `candidate`: il matching lessicale tra sintesi italiana e trascrizioni inglesi non e sufficiente per approvare una citazione senza revisione.

## Prossimo controllo

Per completare la copertura occorre aggiungere al blocco editoriale un riferimento ai `segment_id` di origine. In questo modo si potra calcolare:

`segmenti classificati -> segmenti sintetizzati -> segmenti verificati -> segmenti approvati`

Finche questo collegamento non esiste, i capitoli sono una sintesi iniziale e non una trasposizione completa del corpus.
