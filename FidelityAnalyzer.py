import numpy as np

class FidelityAnalyzer:
    @staticmethod
    def analyze_by_error(original_y, coeffs, threshold=1.0, mode='max_error'):
        """
        Znajduje minimalne K (liczbę współczynników), aby błąd w czasie był poniżej progu.
        
        Args:
            original_y: Oryginalne wartości sygnału (y)
            coeffs: Wszystkie współczynniki FFT (np.fft.rfft)
            threshold: Dopuszczalny błąd (np. 1.0 jednostka amplitudy lub % MSE)
            mode: 'max_error' (Max Absolute Error) lub 'mse' (Mean Squared Error)
            
        Returns:
            dict: {k_threshold, final_error, reconstructed_y}
        """
        N = len(original_y)
        magnitudes = np.abs(coeffs)
        # Sortujemy indeksy współczynników od najsilniejszego do najsłabszego
        sorted_indices = np.argsort(magnitudes)[::-1]
        
        reconstructed_y = np.zeros(N)
        k_min = 0
        current_error = float('inf')

        # Iteracyjnie dodajemy współczynniki i sprawdzamy błąd w dziedzinie czasu
        # Uwaga: Dla wydajności w pętli używamy irfft
        for k in range(1, len(coeffs) + 1):
            # Tworzymy maskę: zostawiamy k najsilniejszych współczynników
            active_indices = sorted_indices[:k]
            test_coeffs = np.zeros_like(coeffs)
            test_coeffs[active_indices] = coeffs[active_indices]
            
            # Powrót do dziedziny czasu
            y_hat = np.fft.irfft(test_coeffs, n=N)
            
            # Obliczanie błędu
            if mode == 'max_error':
                current_error = np.max(np.abs(original_y - y_hat))
            else: # mse
                current_error = np.mean(np.square(original_y - y_hat))
            
            if current_error <= threshold:
                k_min = k
                reconstructed_y = y_hat
                break
        
        return {
            "k_threshold": k_min,
            "final_error": current_error,
            "reconstructed_y": reconstructed_y,
            "mode": mode
        }