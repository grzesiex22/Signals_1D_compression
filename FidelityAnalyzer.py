import numpy as np
from Fourier import DiscreteFourier
from EnergyAnalyzer import EnergyAnalyzer

class FidelityAnalyzer:  
    @staticmethod
    def analyze_by_error(original_y, coeffs, threshold=1.0, mode='max_error', use_numpy=True):
        """
        Znajduje minimalne K (liczbę współczynników), aby błąd w czasie był poniżej progu. 
        Wykorzystuje metodę bisekcji (Binary Search) zamiast liniowego przeszukiwania, co znacząco przyspiesza proces dla dużych N.
        
        Args:
            original_y: Oryginalne wartości sygnału (y)
            coeffs: Wszystkie współczynniki FFT (f_omega_vec)
            threshold: Dopuszczalny błąd (max_allowed_diff)
            mode: 'max_error' (Max Absolute Error) lub 'mse' (Mean Squared Error)
            use_numpy: Flaga wyboru silnika obliczeniowego (True=NumPy, False=Autorski)
            
        Returns:
            dict: {k_threshold, final_error, reconstructed_y, mode}
        """
        N = len(original_y)
        
        # Krok 1. Sortowanie spektralne współczynników
        magnitudes = np.abs(coeffs)
        sorted_indices = np.argsort(magnitudes)[::-1]
        
        reconstructed_y = np.zeros(N)
        k_min = N
        final_error = float('inf')

        # Krok 2. Prekalkulacja macierzy bazowej IDFT
        if not use_numpy:
            k_idx = np.arange(N)
            n_idx = np.arange(N)
            K_mat, N_mat = np.meshgrid(k_idx, n_idx, indexing='ij')
            W_inv_T = np.exp(2j * np.pi * K_mat * N_mat / N).T / N

        # Krok 3. Inicjalizacja wskaźników bisekcji
        low = 1
        high = N

        # Krok 4. Pętla bisekcji (Złożoność O(log M) zamiast O(M))
        while low <= high:
            mid = (low + high) // 2
            
            # Dynamiczne przycinanie dla punktu środkowego 'mid'
            active_indices = sorted_indices[:mid]
            test_coeffs = np.zeros_like(coeffs)
            test_coeffs[active_indices] = coeffs[active_indices]
            
            # Rekonstrukcja sygnału (BLAS / IDFT)
            if use_numpy:
                y_hat = np.fft.ifft(test_coeffs, n=N).real
            else:
                y_hat = np.dot(W_inv_T, test_coeffs).real
            
            # Obliczenie błędu
            if mode == 'max_error':
                current_error = np.max(np.abs(original_y - y_hat))
            else: # mse
                current_error = np.mean(np.square(original_y - y_hat))
            
            # Krok 5. Weryfikacja warunku stopu bisekcji
            if current_error <= threshold:
                # Błąd jest akceptowalny -> zapamiętujemy to jako potencjalne K, 
                # ale szukamy dalej w lewej połówce (może mniejsze K też da radę?)
                k_min = mid
                final_error = current_error
                reconstructed_y = y_hat
                high = mid - 1
            else:
                # Błąd za duży -> musimy wziąć więcej współczynników, szukamy w prawej połówce
                low = mid + 1
        
        return {
            "k_threshold": k_min,
            "final_error": final_error,
            "reconstructed_y": reconstructed_y,
            "mode": mode
        }

