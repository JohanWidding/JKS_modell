# JKS forenklede samfunnsøkonomisk analyse av veiprosjekter

Dette repoet er laget i et prosjekt for å forenkle metoden for å beregne trafikantnytten av utbedring eller nybygging av vei. Modellen skiller mellom gammel vei (alternativ 0) og ny vei (alternativ 1) og bruker endringen av nøkkelfaktorer som tidsbruk og antall kilometer for trafikantene som utgangspunkt for å beregne netto trafikantnytte. Trafikantnytten følger grunnleggende samfunnsøkonomiske prinsipper som tilbud og etterspørsel etter vei er en konsekvens av kostnadene for å bruke veien. 

Fordelen med denne forenklede modellen er flerfoldig. For det første sikrer den transparens slik at det er enkelt å tolke resultatene. For det andre åpner modellen opp for videre modellering gjennom justering av inputfaktorene. Dette betyr at den kan brukes i tilfeller når man er ute etter å teste ulike fremtidsscenarier.

## Innhold

- [Installering](#installering)
- [Bruk](#bruk)

## Installering

Stegvis veiledning for installasjon av prosjektet:

```bash
# I mappen du ønsker at prosjektet skal lagres:
git clone https://github.com/JohanWidding/JKS_modell.git

# Gå inn i mappen
cd JKS_modell

# Installer pakkene som trengs
pip install -r requirements.txt

# Kjør main og se til at alt fungerer som det skal
python main.py
```

## Bruk

Denne applikasjonen lar brukeren simulere trafikantnytte ved å analysere nøkkelfaktorer som tidsbruk og kostnader for gammel og ny vei. Resultatene gir innsikt i netto trafikantnytte, som kan brukes til å støtte beslutninger om veiprosjekter. Modellen gir mulighet for å:

1. **Justere inputfaktorer:** Brukeren kan endre variabler som påvirker tidsbruk, avstand og kostnader osv. i `data/Prosjekter.xlsx`:
   - Ark "data" inneholder prosjektene kolonnevis. Modellen leser dette arket per kolonne som individuelle prosjekter.
     - Radene representerer over 100 ulike parametere som kan endres etter brukerens ønsker. Les beskrivelsen grundig. Dersom variabelnavnet ikke strekker til, se "README"-arket.
   - Ark "Tabell prisvekst" inneholder tabell for nominell prisvekst årene før sammenligningsåret.
   - Ark "Tabell lønnsvekst" inneholder tabell for nominell lønnsvekst årene før sammenligningsåret.
   - Ark "README" inneholder antagelser og premisser som underbygger inputverdiene i modellen.

2. **Analysere resultater:** Modellen genererer rapporter i mappen "Output", én Excel-fil per prosjekt. Denne dataen kan videre brukes til analyser.

3. **Teste fremtidsscenarier:** Med mulighet for å justere ulike antagelser og inputverdier i `Prosjekter.xlsx` kan modellen brukes til å evaluere potensielle utviklinger over tid.

For å starte applikasjonen, følg disse stegene:

1. Sørg for at alle avhengigheter er installert ved å følge installasjonsinstruksjonene.
2. Kjør `main.py` for å starte hovedapplikasjonen.
3. Se mappen "Output" for de genererte rapportene.

For mer informasjon om hvordan du bruker spesifikke funksjoner i modellen, se dokumentasjonen i prosjektet eller kontakt utvikleren via GitHub.