class Project():
    def __init__(self, project_name, var_names, var_values, price_growth, wage_growth):
        # Denne metoden initialiserer en Project-instans ved å dynamisk opprette attributter basert på to lister:
        # var_names: en liste med navnene på attributtene som skal opprettes.
        # var_values: en liste med verdier som skal tildeles de tilsvarende attributtene.
        # For hver indeks i var_values, opprettes et attributt med navnet fra var_names[i]
        # og tildeles verdien fra var_values[i] ved bruk av setattr-funksjonen.
        self.name = project_name
        self.price_growth_df = price_growth
        self.wage_growth_df = wage_growth
        for i, value in enumerate(var_values):
            setattr(self, var_names[i], value)
