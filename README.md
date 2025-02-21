# JKS Forenklet Samfunnsøkonomisk Analyse av Veiprosjekter

Denne modellen er utviklet for å forenkle beregningen av trafikantnytte ved utbedring eller nybygging av veier. Modellen skiller mellom eksisterende vei (alternativ 0) og ny vei (alternativ 1) og bruker endringen i nøkkelfaktorer som tidsbruk og reiselengde for å beregne netto trafikantnytte. Modellen bygger på grunnleggende samfunnsøkonomiske prinsipper, hvor etterspørselen etter vei er en funksjon av kostnadene for å bruke den.

Fordelene med denne forenklede modellen inkluderer:
- **Transparens:** Enkle og lett tolkelige resultater.
- **Fleksibilitet:** Mulighet for justering av inputfaktorer.
- **Scenariotesting:** Kan brukes til å evaluere ulike fremtidige utviklinger.
- **Risikoanalyse:** Egner seg for sammenligning av flere prosjekter med felles forutsetninger.

## Innhold

- [Installasjon](#installasjon)
- [Bruk](#bruk)

## Installasjon

Følg disse stegene for å installere prosjektet:

```bash
# Last ned prosjektet
git clone https://github.com/JohanWidding/JKS_modell.git

# Gå til prosjektmappen
cd JKS_modell

# Installer nødvendige pakker
pip install -r requirements.txt

# Kør hovedscriptet for å teste installasjonen
python main.py
```

## Bruk

Denne applikasjonen lar brukeren simulere trafikantnytte ved å analysere nøkkelfaktorer som tidsbruk og kostnader for eksisterende og ny vei. Resultatene gir innsikt i netto trafikantnytte, som kan brukes til å støtte beslutninger om veiprosjekter.

### 1. Justering av inputfaktorer
Brukeren kan endre variabler som påvirker tidsbruk, avstand og kostnader i `data/Prosjekter.xlsx`. Strukturen er som følger:

- **Ark "data"**: Inneholder prosjektene og deres scenarier kolonnevis. Modellen leser hver kolonne som et prosjekt. Dersom et prosjektnavn har flere scenarier (f.eks. "E39 - Lav vekst", "E39 - Høy vekst"), vil modellen kategorisere disse under prosjektet "E39" med tilhørende scenarier.
- **Ark "Tabell prisvekst"**: Inneholder tabell for nominell prisvekst for årene før sammenligningsåret.
- **Ark "Tabell lønnsvekst"**: Inneholder tabell for nominell lønnsvekst for årene før sammenligningsåret.
- **Ark "README"**: Beskriver antagelser og premisser bak inputverdiene.
- **Ark "Befolkningsfremskrivelser"**: Inneholder regionale befolkningsfremskrivelser for personer over 18 år (fra SSB).
    - Opddater arket med dette APIet: https://github.com/JohanWidding/SSB-regionale-befolkningsframskrivinger
    - Lim inn de nye verdiene

### 2. Kør modellen
Start modellen ved å kjøre `main.py`:

```bash
python main.py
```

For at modellen skal fungere riktig, må fil- og parameterreferanser samsvare i:
- `functions/data_management/load_project_data.py`
- `data/keyword_mapping.txt`
- `data/Prosjekter.xlsx`

### 3. Analyse av resultater
Modellen genererer rapporter i `Output`-mappen, hvor hver Excel-fil representerer et prosjekt-scenario. Dataene oppsummeres i `projects_data.xlsx`, som gir en overordnet oversikt over vurderte prosjekter.

### Riktig bruk av inputfaktorer
For realistiske analyser er det viktig at inputverdiene i `Prosjekter.xlsx` reflekterer sannsynlige utviklingsbaner. Feil eller ekstreme verdier kan gi misvisende resultater.

## Videre utvikling
Modellen er bygd for å være lett å forstå og videreutvikle. Nedenfor er stegene for å legge til en ny parameter:

1. Legg til en ny rad i "data"-arket i `Prosjekter.xlsx`.
2. Oppdater `data/keyword_mapping.txt` med en ny linje:

```txt
hardkodet_navn, brukervennlig_navn
```

Denne mappingen gjør det mulig å referere til parameteren i modellen via objektet `Prosjekt`:

```python
project.region
project.dette_er_min_nye_parameter
```

### Navigering i modellen
For å forstå modellens struktur anbefales det å starte fra `main.py`. Den viktigste funksjonen her er `calculate_project()`, som fungerer som en hub for alle beregninger. Funksjonene returnerer hovedsakelig `pandas.DataFrame`-objekter med felles indeks og kolonneoverskrifter, noe som gjør det enkelt å kombinere dem med standard operasjoner (+, -, *, etc.).

## Kort om hvordan den fungerer

Denne modellen beregner trafikkvolum og tilhørende kostnader basert på ulike scenarier for fremtidig kjøretøyflåte. 

### 1. Datainnhenting
Data hentes inn fra `data`-mappen.

### 2. Prosjektgjennomgang
Modellen går gjennom alle prosjektene i datasettet.

### 3. Beregning av ÅDT (Årsdøgntrafikk)
- Scriptet `gen_car_fleet_timeseries.py` brukes for å generere kjøretøyflåten over tid.
- En overgangs-tidserie legges opper, som inneholder multiplikatorverdier for å justere fossildrevne kjøretøy.
- Fossildrevne kjøretøy som fases ut, overføres til elbilparken.
- Elastisiteter benyttes for å estimere trafikkvolumet i nullalternativet.

### 4. Beregning av kostnader
- **Tidskostnader**: Beregning av tidsforbruk og relaterte kostnader.
- **Kjøretøykostnader**: Beregning av driftskostnader per kjøretøy.
- **Konstantledd**: Inkludering av faste kostnader i modellen.

### 5. Beregning av trafikantnytte
Trafikantnytten estimeres basert på beregnede kostnader og endringer i trafikkvolum.

### 6. Diskontering av trafikantnytte
Trafikantnytten diskonteres for å ta hensyn til tidsverdien av nytte.

### 7. Lagring av resultater
Beregningene lagres som enkeltfiler i `Output`-mappen.

### 8. Oppsummering av resultater
Til slutt hentes alle Excel-filene i `Output`-mappen og oppsummeres i `projects_data.xlsx`.

## Videre utvikling
- Vurdere bruk av diskontering for mer realistisk usikkerhet.
- Optimalisering av beregningshastighet for hyppigere bruk.


## Oppsummering
For å bruke modellen effektivt:

1. Installer nødvendige avhengigheter.
2. Juster inputdata i `Prosjekter.xlsx`.
3. Kør `main.py`.
4. Analyser resultatene i `projects_data.xlsx`.

For mer informasjon eller bidrag til utviklingen, ta kontakt via GitHub.

---

Dette README-dokumentet sikrer en klar beskrivelse av prosjektet og hjelper brukere og utviklere med å forstå og videreutvikle modellen.
