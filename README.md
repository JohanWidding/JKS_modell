# JKS Forenklet Samfunnsøkonomisk Analyse av Veiprosjekter

Dette prosjektet er utviklet for å forenkle beregningen av trafikantnytte ved utbedring eller nybygging av veier. Modellen skiller mellom eksisterende vei (alternativ 0) og ny vei (alternativ 1) og bruker endringen i nøkkelfaktorer som tidsbruk og reiselengde for å beregne netto trafikantnytte. Modellen bygger på grunnleggende samfunnsøkonomiske prinsipper, hvor etterspørselen etter vei er en funksjon av kostnadene for å bruke den.

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
- **Ark "Kjøretøypark tunge"**: Trafikkarbeidstidserier for tunge kjøretøy, fordelt på diesel-, elektriske- og hydrogendrevne lastebiler.

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

## Oppsummering
For å bruke modellen effektivt:

1. Installer nødvendige avhengigheter.
2. Juster inputdata i `Prosjekter.xlsx`.
3. Kør `main.py`.
4. Analyser resultatene i "Output"-mappen.

For mer informasjon eller bidrag til utviklingen, ta kontakt via GitHub.

---

Dette README-dokumentet sikrer en klar beskrivelse av prosjektet og hjelper brukere og utviklere med å forstå og videreutvikle modellen.
