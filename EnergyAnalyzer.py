import numpy as np

class EnergyAnalyzer:
    @staticmethod
    def calculate_total_energy(signal_data_y):
        """Oblicza całkowitą energię sygnału w dziedzinie czasu."""
        # Energia sygnału dyskretnego to suma kwadratów jego wartości
        return np.sum(np.square(signal_data_y))

    @staticmethod
    def analyze_energy_distribution(coeffs, N, threshold=0.95):
        """
        Analizuje rozkład energii w widmie Fouriera.
        
        Args:
            coeffs: Współczynniki FFT (wynik np.fft.rfft)
            N: Liczba próbek sygnału
            threshold: Próg zachowania energii (domyślnie 95%)
            
        Returns:
            dict: Statystyki energii (E_total, K_threshold, energy_vector)
        """
        # 1. Moc każdej składowej (kwadrat modułu współczynnika)
        # Uwaga: rfft zwraca wartości zespolone, bierzemy ich moduł
        power_spectrum = np.abs(coeffs)**2
        
        # 2. Całkowita energia w dziedzinie częstotliwości
        total_energy_freq = np.sum(power_spectrum) / N
        
        # 3. Sortowanie składowych od najsilniejszej do najsłabszej
        sorted_powers = np.sort(power_spectrum)[::-1]
        
        # 4. Suma skumulowana energii
        cumulative_energy = np.cumsum(sorted_powers) / np.sum(power_spectrum)
        
        # 5. Znalezienie K (liczba składowych powyżej progu)
        k_threshold = np.argmax(cumulative_energy >= threshold) + 1
        
        return {
            "total_energy_freq": total_energy_freq,
            "k_threshold": k_threshold,
            "cumulative_energy": cumulative_energy
        }