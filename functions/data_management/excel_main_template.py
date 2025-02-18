import pandas as pd
from xlsxwriter.utility import xl_range

from functions.data_management.output_overview import overview_to_excel

def dump_projects_to_excel(files_dict, output_file):
    """
    Eksporterer prosjektdata til en Excel-fil med ett ark per prosjekt.
    
    Format:
      - Rad 0: Tittel (prosjektnavn) – fontstørrelse 16, venstrejustert.
      - Rad 1: Blank rad.
      - Rad 2: Oversiktsheader: "Parameter", "Verdi", "Prosent avvik" (fet med bunnlinje).
      - Rad 3: Baseverdi (kursiv); verdi og prosentavvik (i forhold til Baseverdi),
               med en stiplet (dotted) bunnlinje.
      - Rad 4: Blank rad.
      - Rad 5: Øvre – verdi og prosentavvik (i forhold til Baseverdi).
      - Rad 6: Nedre – verdi og prosentavvik (i forhold til Baseverdi).
      - Rad 7: Blank rad.
      - Rad 8: EFFEKT Trafikantnytte – verdi og prosentavvik (i forhold til Baseverdi), med bunnlinje.
      - Rad 9: Blank rad.
      - Rad 10: Scenario-tabell header ("Scenario" + scenarienavn), med bunnlinje.
      - Rad 11 og nedover: Scenario-tabellens data.
    
    I tillegg vil alle celler fra A til D (kolonne 0 til 3) og fra rad 1 til 20 ha hvit bakgrunn,
    og cellene med scenario-tabellverdier vil få en heatmap-formatert bakgrunn.
    
    Parameters:
      files_dict (dict): Struktur
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

    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        writer = overview_to_excel(files_dict, writer)
        for project, scenarios in files_dict.items():
            # Begrens arknavnet til 31 tegn
            sheet_name = project[:31]
            workbook = writer.book
            worksheet = workbook.add_worksheet(sheet_name)
            writer.sheets[sheet_name] = worksheet

            # --------------------------------------------------
            # Definer formater med hvit bakgrunn
            # --------------------------------------------------
            title_format = workbook.add_format({
                "bold": True,
                "align": "left",
                "font_size": 16,
                "bg_color": "white"
            })
            money_format = workbook.add_format({
                "num_format": "#,##0",
                "align": "center",
                "bg_color": "white"
            })
            center_percent_format = workbook.add_format({
                "num_format": "0.00%",
                "align": "center",
                "bg_color": "white"
            })
            bold_center_format = workbook.add_format({
                "bold": True,
                "align": "center",
                "bg_color": "white"
            })
            # Header for oversiktsblokken – fet med bunnlinje
            header_format0 = workbook.add_format({
                "bold": True,
                "align": "right",
                "bg_color": "white",
                "bottom": 1
            })
            header_format1 = workbook.add_format({
                "bold": True,
                "align": "center",
                "bg_color": "white",
                "bottom": 1
            })
            header_format2 = workbook.add_format({
                "bold": True,
                "align": "center",
                "bg_color": "white",
                "bottom": 1
            })
            # Oversiktsetiketter (kursiv, høyrejustert)
            summary_label_format = workbook.add_format({
                "italic": True,
                "align": "right",
                "bg_color": "white"
            })
            # Baseverdi-format med DOTTED bunnlinje (bruker bottom: 4 for å indikere stiplet linje)
            base_label_dotted = workbook.add_format({
                "italic": True,
                "align": "right",
                "bg_color": "white",
                "bottom": 4
            })
            base_money_dotted = workbook.add_format({
                "num_format": "#,##0",
                "align": "center",
                "bg_color": "white",
                "bottom": 4
            })
            base_percent_dotted = workbook.add_format({
                "num_format": "0.00%",
                "align": "center",
                "bg_color": "white",
                "bottom": 4
            })
            # Effekt-raden: kursiv med bunnlinje
            effekt_label_border = workbook.add_format({
                "italic": True,
                "align": "right",
                "bg_color": "white",
                "bottom": 1
            })
            effekt_money_border = workbook.add_format({
                "num_format": "#,##0",
                "align": "center",
                "bg_color": "white",
                "bottom": 1
            })
            effekt_percent_format = workbook.add_format({
                "num_format": "0.00%",
                "align": "center",
                "bg_color": "white",
                "bottom": 1
            })
            # Scenario-tabell header: fet, sentrert med bunnlinje
            scenario_header_format = workbook.add_format({
                "bold": True,
                "align": "center",
                "bg_color": "white",
                "bottom": 1
            })
            # Format for scenario-etiketter (kursiv, venstrejustert)
            scenario_label_format = workbook.add_format({
                "italic": True,
                "align": "left",
                "bg_color": "white"
            })

            # --------------------------------------------------
            # Sett kolonnebredder (A til D)
            # --------------------------------------------------
            worksheet.set_column(0, 0, 25)  # Kolonne A bredere
            worksheet.set_column(1, 3, 18)  # Kolonne B til D

            # --------------------------------------------------
            # Hent data fra 'Main'/'Standard'
            # --------------------------------------------------
            base_value = None
            effect_value = None
            if "Main" in scenarios:
                for file_obj in scenarios["Main"]:
                    if file_obj.variation == "Hovedalternativet (MMMM)" and not file_obj.df.empty:
                        base_value = clean_int(file_obj.df.iloc[0, -1])
                        effect_value = clean_int(file_obj.df.iloc[1, -1]) if file_obj.df.shape[0] > 1 else 0
                        break
            if base_value is None or base_value == 0:
                base_value = 1
            if effect_value is None or effect_value == 0:
                effect_value = 1

            # Samle øvre verdi fra alle file_obj (kun øvre høyre celle)
            values = []
            for scenario in scenarios.values():
                for file_obj in scenario:
                    if not file_obj.df.empty:
                        cost = clean_int(file_obj.df.iloc[0, -1])
                        values.append(cost)
            lower_value = min(values) if values else base_value
            upper_value = max(values) if values else base_value

            # --------------------------------------------------
            # Beregn prosentavvik i forhold til Baseverdi
            # --------------------------------------------------
            base_dev   = 0
            upper_dev  = (upper_value - base_value) / base_value
            lower_dev  = (lower_value - base_value) / base_value
            effekt_dev = (effect_value - base_value) / base_value

            # --------------------------------------------------
            # Definer radindekser
            # --------------------------------------------------
            row_title             = 0   # Tittel
            row_blank_after_title = 1   # Blank rad
            row_summary_header    = 2   # Oversiktsheader
            row_base              = 3   # Baseverdi-rad
            row_blank_after_base  = 4   # Blank rad
            row_upper             = 5   # Øvre
            row_lower             = 6   # Nedre
            row_blank_after_ul    = 7   # Blank rad
            row_effekt            = 8   # Effekt-rad
            row_blank_after_eff   = 9   # Blank rad
            row_scenario_header   = 10  # Scenario-tabell header
            row_scenario_data     = 11  # Scenario-tabell data starter her

            # --------------------------------------------------
            # Skriv ut oversiktsdelen
            # --------------------------------------------------
            worksheet.write(row_title, 0, project, title_format)
            # Rad 1 er blank.
            worksheet.write(row_summary_header, 0, "Parameter", header_format0)
            worksheet.write(row_summary_header, 1, "Verdi", header_format1)
            worksheet.write(row_summary_header, 2, "Prosent avvik", header_format2)
            
            # Baseverdi (rad 3) med DOTTED bunnlinje
            worksheet.write(row_base, 0, "Baseverdi", base_label_dotted)
            worksheet.write(row_base, 1, base_value, base_money_dotted)
            worksheet.write(row_base, 2, base_dev, base_percent_dotted)
            
            # Blank rad (rad 4)
            # Øvre (rad 5)
            worksheet.write(row_upper, 0, "Øvre", summary_label_format)
            worksheet.write(row_upper, 1, upper_value, money_format)
            worksheet.write(row_upper, 2, upper_dev, center_percent_format)
            
            # Nedre (rad 6)
            worksheet.write(row_lower, 0, "Nedre", summary_label_format)
            worksheet.write(row_lower, 1, lower_value, money_format)
            worksheet.write(row_lower, 2, lower_dev, center_percent_format)
            
            # Blank rad (rad 7)
            # Effekt Trafikantnytte (rad 8) med bunnlinje
            worksheet.write(row_effekt, 0, "EFFEKT Trafikantnytte", effekt_label_border)
            worksheet.write(row_effekt, 1, effect_value, effekt_money_border)
            worksheet.write(row_effekt, 2, effekt_dev, effekt_percent_format)
            
            # Blank rad (rad 9)
            # Scenario-tabell header (rad 10)
            worksheet.write(row_scenario_header, 0, "Scenario", scenario_header_format)
            scenario_names = list(scenarios.keys())
            for col_idx, scenario in enumerate(scenario_names, start=1):
                scenario = "Base" if scenario == "Main" else scenario
                worksheet.write(row_scenario_header, col_idx, scenario, scenario_header_format)
            
            # Scenario-tabell data (rad 11 og nedover)
            variations = set()
            for scenario in scenarios.values():
                for file_obj in scenario:
                    variations.add(file_obj.variation)
            variations = sorted(variations)
            for row_idx, variation in enumerate(variations, start=row_scenario_data):
                worksheet.write(row_idx, 0, variation, scenario_label_format)
                for col_idx, scenario in enumerate(scenario_names, start=1):
                    file_objs = scenarios.get(scenario, [])
                    value = ""
                    for file_obj in file_objs:
                        if file_obj.variation == variation and not file_obj.df.empty:
                            value = clean_int(file_obj.df.iloc[0, -1])
                            break
                    worksheet.write(row_idx, col_idx, value, money_format)
            
            # --------------------------------------------------
            # Påfør en conditional formatting (heatmap) for scenario-tabellens verdiceller.
            # Området går fra første data celle i scenario-tabellen (rad_scenario_data, kolonne 1)
            # til siste rad og siste scenario-kolonne.
            # --------------------------------------------------
            num_variations = len(variations)
            num_scenarios = len(scenario_names)
            if num_variations > 0 and num_scenarios > 0:
                # Beregn området for scenario-tabellens data (fra rad row_scenario_data, kolonne 1 til siste scenario-kolonne)
                num_variations = len(variations)
                num_scenarios = len(scenario_names)
                if num_variations > 0 and num_scenarios > 0:
                    data_range = xl_range(row_scenario_data, 1, row_scenario_data + num_variations - 1, num_scenarios)
                    worksheet.conditional_format(data_range, {
                        'type': '3_color_scale',
                        'min_color': "#5B9BD5",   # Blå – representerer kalde (lave) verdier
                        'mid_color': "#FFEB84",   # Midt: gul (som tidligere)
                        'max_color': "#F8696B"    # Rød – for høye verdier
                    })
            
            # --------------------------------------------------
            # Sørg for at alle celler fra A1 til D20 har hvit bakgrunn
            # --------------------------------------------------
            white_bg_format = workbook.add_format({"bg_color": "white"})
            worksheet.conditional_format('A1:M20', {
                'type': 'formula',
                'criteria': '=TRUE',
                'format': white_bg_format
            })
            
        return output_file
