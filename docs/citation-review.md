# Revisione delle citazioni

## Stato

La coda di revisione contiene `144` associazioni tra blocchi approvati e intervalli timestamp candidati.

Questi intervalli sono stati trovati con matching lessicale limitato alla fonte associata. Sono utili per accelerare il controllo, ma non sono ancora citazioni approvate.

## Criterio di approvazione

Una citazione puo passare a `verified` solo se il segmento:

- appartiene alla fonte corretta;
- ricade nell'intervallo timestamp indicato;
- sostiene il significato completo del blocco;
- non viene usato per attribuire al relatore una conclusione che non ha espresso;
- e coerente con eventuali qualificazioni, limiti o condizioni presenti nella fonte.

Se il segmento sostiene solo una parte del blocco, occorre restringere il blocco, aggiungere una seconda fonte oppure lasciare lo stato `candidate`.

## Stati

- `candidate`: associazione automatica da verificare;
- `verified`: controllata contro la trascrizione e approvata;
- `rejected`: non sostiene il blocco;
- `needs-source`: serve la fonte originale o un timestamp piu preciso.

## Procedura

1. aprire un elemento in `docs/citation-review.json`;
2. cercare `source_id`, `segment_id` e timestamp nella trascrizione di lavorazione esterna;
3. confrontare il testo del segmento con il blocco editoriale;
4. aggiornare lo stato e la nota di revisione;
5. rigenerare l'indice senza sovrascrivere le decisioni gia verificate.

L'approvazione editoriale di Andrea riguarda i contenuti dei blocchi. Questa coda riguarda esclusivamente la precisione della provenienza.
