import numpy as np
import pandas as pd 
from FidelityAnalyzer import FidelityAnalyzer
from Plotter import Plotter
from Fourier import DiscreteFourier

class FidelityTester:
    def __init__(self, dataset):
        """
        Inicjalizacja testera.
        Args:
            dataset (dict): Słownik list sygnałów (np. z DatasetCreator)
        """
        self.dataset = dataset
        self.results = {}

    def run(self, threshold=2.0, mode='mse', use_custom_fft=False):
        """
        Uruchamia testy dla wszystkich sygnałów w zbiorze.
        """
        self.results = {}
        
        for category, signals in self.dataset.items():
            print(f"Przetwarzanie kategorii: {category.upper()}...")
            k_values = []
            
            for i, signal in enumerate(signals):
                if use_custom_fft:
                    _, coeffs = DiscreteFourier.transform(signal.t, signal.y)
                    print(f"{category}, {i}")
                else:
                    coeffs = np.fft.fft(signal.y)
                
                analysis = FidelityAnalyzer.analyze_by_error(
                    original_y=signal.y, 
                    coeffs=coeffs, 
                    threshold=threshold, 
                    mode=mode,
                    use_numpy=not use_custom_fft
                )
                
                k_values.append(analysis['k_threshold'])
            
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
        
        # Wyrzucamy współczynniki k aby ich nie drukować w terminalu
        if "k_list" in df.columns:
            df = df.drop(columns=["k_list"])
        return df