import numpy as np
import pandas as pd # Opcjonalnie do ładnego wyświetlania tabeli
from FidelityAnalyzer import FidelityAnalyzer
from Plotter import Plotter

class FidelityTester:
    def __init__(self, dataset):
        """
        Inicjalizacja testera.
        Args:
            dataset (dict): Słownik list sygnałów (np. z DatasetCreator)
        """
        self.dataset = dataset
        self.results = {}

    def run(self, threshold=2.0, mode='mse'):
        """
        Uruchamia testy dla wszystkich sygnałów w zbiorze.
        """
        self.results = {}
        
        for category, signals in self.dataset.items():
            print(f"Przetwarzanie kategorii: {category.upper()}...")
            k_values = []
            
            for i, signal in enumerate(signals):
                # 1. Transformata FFT
                coeffs = np.fft.rfft(signal.y)
                
                # 2. Analiza wierności (wykorzystujemy Twoją klasę FidelityAnalyzer)
                analysis = FidelityAnalyzer.analyze_by_error(
                    original_y=signal.y, 
                    coeffs=coeffs, 
                    threshold=threshold, 
                    mode=mode
                )
                
                # 3. Zapisujemy wynik K
                k_values.append(analysis['k_threshold'])
            
            # 4. Agregacja wyników dla kategorii
            self.results[category] = {
                "category": category,
                "k_list": k_values,
                "mean_k": np.mean(k_values),
                "std_k": np.std(k_values),
                "min_k": np.min(k_values),
                "max_k": np.max(k_values),
                "count": len(k_values)
            }

        print("Analiza zakończona.\n")
        return self.results

    def display_results(self):
        """Wyświetla wyniki w formie czytelnej tabeli."""
        df = pd.DataFrame(self.results).T
        
        for index, cat in df.iterrows():
            Plotter.plot_k_histogram(k=cat["k_list"],
                                        title=f"Histogram współczynników Fouriera dla sygnałów {cat['category']}")
        
        # Usuwamy listę surowych danych K dla lepszej czytelności tabeli
        if "k_list" in df.columns:
            df = df.drop(columns=["k_list"])
        return df