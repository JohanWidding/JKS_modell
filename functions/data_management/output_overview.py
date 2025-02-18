import pandas as pd
from xlsxwriter.utility import xl_range

def overview_to_excel(files_dict, writer):
    """
    Eksporterer et sammendragsark ("Overview") med tre tabeller basert på data fra alle prosjekter.
    
    For hvert prosjekt beregnes:
      - Trafikantnytte JKSM (baseverdi) og EFFEKT, hentet fra scenario "Main" med varianten "Standard".
      - Nedre og Øvre: henholdsvis den laveste og høyeste verdien (øverste høyre celle) fra alle filobjekter.
      - Prosentavvik beregnes med JKSM som nevner:
            EFFEKT-avvik = (EFFEKT - JKSM) / JKSM  
            Nedre-avvik = (Nedre - JKSM) / JKSM  
            Øvre-avvik = (Øvre - JKSM) / JKSM
    
    Sammendragsarket ("Overview") består av tre tabeller side om side:
      Tabell 1 (venstre): Prosjekt, Trafikantnytte EFFEKT, Trafikantnytte JKSM, Prosent avvik (EFFEKT)
      Tabell 2 (midt):  Prosjekt, Trafikantnytte JKSM, Nedre, Øvre
      Tabell 3 (høyre):  Prosjekt, Nedre prosentavvik, Øvre prosentavvik

    Merk: Alle beløp konverteres til milliarder (dividert med 1e9), og JKSM er benyttet som referanse (baseverdi).
    
    Parameters:
      files_dict (dict): Struktur:
          {
              "ProjectName": {
                  "ScenarioName1": [file_obj1, file_obj2, ...],
                  "ScenarioName2": [file_obj3, ...],
                  ...
              },
              ...
          }
          hvor hvert file_obj har:
              - variation (str): Variasjonens navn.
              - df (pandas DataFrame): Dataene.
      output_file (str): Filnavn for eksportert Excel-fil.
    """
    def clean_int(value):
        try:
            return int(str(value).replace(" ", "").replace(",", ""))
        except ValueError:
            return 0

    # Samle sammendragsdata for hvert prosjekt
    summary_data = []
    for project, scenarios in files_dict.items():
        # Hent ut Trafikantnytte JKSM (base) og EFFEKT fra scenario "Main"/"Standard"
        base_value = None  # JKSM
        effect_value = None  # EFFEKT
        if "Main" in scenarios:
            for file_obj in scenarios["Main"]:
                if file_obj.variation == "Hovedalternativet (MMMM)" and not file_obj.df.empty:
                    base_value = clean_int(file_obj.df.iloc[0, -1])
                    effect_value = clean_int(file_obj.df.iloc[1, -1]) if file_obj.df.shape[0] > 1 else 0
                    break
        if base_value is None or base_value == 0:
            base_value = 1  # Unngå divisjon på null
        if effect_value is None or effect_value == 0:
            effect_value = 1

        # Samle alle kostnadsverdier (øverste høyre celle) fra prosjektet
        values = []
        for scenario in scenarios.values():
            for file_obj in scenario:
                if not file_obj.df.empty:
                    cost = clean_int(file_obj.df.iloc[0, -1])
                    values.append(cost)
        lower_value = min(values) if values else base_value
        upper_value = max(values) if values else base_value

        # Prosentberegninger (alle i forhold til JKSM)
        effect_dev = (effect_value - base_value) / base_value
        lower_dev = (lower_value - base_value) / base_value
        upper_dev = (upper_value - base_value) / base_value

        summary_data.append({
            "project": project,
            "trafikantnytte_effekt": effect_value / 1e9,
            "trafikantnytte_jksm": base_value / 1e9,
            "prosent_avvik": effect_dev,
            "nedre": lower_value / 1e9,
            "ovre": upper_value / 1e9,
            "nedre_prosent": lower_dev,
            "ovre_prosent": upper_dev
        })
    
    # Sorter prosjektene etter størst relativt/prosent avvik mellom Nedre og Øvre
    summary_data.sort(key=lambda d: d["ovre_prosent"] - d["nedre_prosent"], reverse=True)


    workbook = writer.book
    overview_sheet = workbook.add_worksheet("Oversikt")
    writer.sheets["Oversikt"] = overview_sheet

    # Flytt tabellen ett hakk ned: header starter nå på rad 1
    header_row = 1
    data_row = header_row + 1  # data starter på rad 2

    # Definer formater med hvit bakgrunn og border under header-labels
    header_format = workbook.add_format({
        "bold": True,
        "align": "center",
        "bg_color": "white",
        "bottom": 1  # Legger til en border under header cellene
    })
    text_format = workbook.add_format({
        "align": "left",
        "bg_color": "white"
    })
    money_format = workbook.add_format({
        "num_format": "##,##0.00 \"mrd\"",
        "align": "center",
        "bg_color": "white"
    })
    percent_format = workbook.add_format({
        "num_format": "0.00%",
        "align": "center",
        "bg_color": "white"
    })

    # Flytt tabellene ett hakk mot høyre:
    table1_start_col = 8   # Tabell 1 starter i kolonne B
    table2_start_col = 13   # Tabell 2 starter i kolonne G
    table3_start_col = 1  # Tabell 3 starter i kolonne L

    # --- Tabell 1: Prosjekt, Trafikantnytte EFFEKT, Trafikantnytte JKSM, Prosent avvik ---
    overview_sheet.write(header_row, table1_start_col + 0, "Prosjekt", header_format)
    overview_sheet.write(header_row, table1_start_col + 1, "Trafikantnytte EFFEKT", header_format)
    overview_sheet.write(header_row, table1_start_col + 2, "Trafikantnytte JKSM", header_format)
    overview_sheet.write(header_row, table1_start_col + 3, "Prosent avvik", header_format)

    # --- Tabell 2: Prosjekt, Trafikantnytte JKSM, Nedre, Øvre ---
    overview_sheet.write(header_row, table2_start_col + 0, "Prosjekt", header_format)
    overview_sheet.write(header_row, table2_start_col + 1, "Trafikantnytte JKSM", header_format)
    overview_sheet.write(header_row, table2_start_col + 2, "Nedre", header_format)
    overview_sheet.write(header_row, table2_start_col + 3, "Øvre", header_format)

    # --- Tabell 3: Prosjekt, Nedre prosentavvik, Øvre prosentavvik ---
    overview_sheet.write(header_row, table3_start_col + 0, "Prosjekt", header_format)
    overview_sheet.write(header_row, table3_start_col + 1, "Nedre prosentavvik", header_format)
    overview_sheet.write(header_row, table3_start_col + 2, "Øvre prosentavvik", header_format)
    overview_sheet.write(header_row, table3_start_col + 3, "Nedre Trafikantnytte", header_format)
    overview_sheet.write(header_row, table3_start_col + 4, "EFFEKT Trafikantnytte", header_format)
    overview_sheet.write(header_row, table3_start_col + 5, "Øvre Trafikantnytte", header_format)

    # Skriv ut dataene – én rad per prosjekt, starter fra data_row
    current_row = data_row
    for data in summary_data:
        # Tabell 1
        overview_sheet.write(current_row, table1_start_col + 0, data["project"], text_format)
        overview_sheet.write(current_row, table1_start_col + 1, data["trafikantnytte_effekt"], money_format)
        overview_sheet.write(current_row, table1_start_col + 2, data["trafikantnytte_jksm"], money_format)
        overview_sheet.write(current_row, table1_start_col + 3, data["prosent_avvik"], percent_format)
        # Tabell 2
        overview_sheet.write(current_row, table2_start_col + 0, data["project"], text_format)
        overview_sheet.write(current_row, table2_start_col + 1, data["trafikantnytte_jksm"], money_format)
        overview_sheet.write(current_row, table2_start_col + 2, data["nedre"], money_format)
        overview_sheet.write(current_row, table2_start_col + 3, data["ovre"], money_format)
        # Tabell 3
        overview_sheet.write(current_row, table3_start_col + 0, data["project"], text_format)
        overview_sheet.write(current_row, table3_start_col + 1, data["nedre_prosent"], percent_format)
        overview_sheet.write(current_row, table3_start_col + 2, data["ovre_prosent"], percent_format)
        overview_sheet.write(current_row, table3_start_col + 3, (1+data["nedre_prosent"])*data["trafikantnytte_effekt"], money_format)
        overview_sheet.write(current_row, table3_start_col + 4, data["trafikantnytte_effekt"], money_format)
        overview_sheet.write(current_row, table3_start_col + 5, (1+data["ovre_prosent"])*data["trafikantnytte_effekt"], money_format)
        current_row += 1

    # Sett bakgrunn og standard kolonnebredde for kolonner A til O
    overview_sheet.set_column('A:Q', 20, workbook.add_format({'bg_color': 'white'}))
    # Overstyr bredden for kolonne A, F og K (mye smalere)
    overview_sheet.set_column('A:A', 10, workbook.add_format({'bg_color': 'white'}))
    overview_sheet.set_column('H:H', 10, workbook.add_format({'bg_color': 'white'}))
    overview_sheet.set_column('M:M', 10, workbook.add_format({'bg_color': 'white'}))

    return writer
