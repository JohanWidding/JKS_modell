import numpy as np

def logistic_decay_values(t0, k=0.2, t_min=0, t_max=1, num_points=76, x=0):
    """
    Returnerer en liste med logistisk synkende verdier for en gitt t0.
    
    Parametere:
    - t0: Midtpunktet for nedgangen.
    - k: Vekstparameter (standard 0.2).
    - t_min: Startår (standard 0).
    - t_max: Sluttår (standard 100).
    - num_points: Antall punkter i listen (standard 200).
    - x: Minimumsverdi mellom 1 og 0 (standard 0).
    
    Returnerer:
    - En liste med årsverdier.
    """
    years = np.linspace(t_min, t_max, num_points)
    values = x + (1 - x) / (1 + np.exp(-k * (t0 - years)))
    return values.tolist()

if __name__ == "__main__":
    result = logistic_decay_values(t0=5, x=0.2)
    print(len(result))  # Viser de første 10 verdiene
