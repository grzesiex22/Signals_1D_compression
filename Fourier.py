import numpy as np
from scipy.integrate import simpson 
import matplotlib.pyplot as plt


class Fourier:
    def __init__(self, t_vec, y_vec):
        """
        t_vec: wektor czasu (np. linspace)
        y_vec: wartości sygnału dla tych punktów czasu
        """
        self.t_vec = t_vec
        self.y_vec = y_vec

    def transform(self, omega_limit=15, num_omega=500):
        """
        Oblicza widmo w zadanym zakresie.
        Zwraca: (omega_vec, f_omega_vec)
        """
        omega_vec = np.linspace(-omega_limit, omega_limit, num_omega)
        
        # Wektoryzacja obliczeń
        exponent = -1j * omega_vec[:, np.newaxis] * self.t_vec
        integrand = self.y_vec * np.exp(exponent)
        f_omega_vec = simpson(y=integrand, x=self.t_vec, axis=1)
        
        return omega_vec, f_omega_vec

    def inverse_transform(self, omega_vec, f_omega_vec):
        """
        Odtwarza sygnał na podstawie podanego widma (f_omega_vec) 
        i odpowiadających mu częstotliwości (omega_vec).
        """
        t = np.atleast_1d(self.t_vec)
        # Tworzymy siatkę dla czasu i częstotliwości
        T, O = np.meshgrid(t, omega_vec, indexing='ij')
        
        # Rozszerzamy widmo do wymiarów macierzy
        F_matrix = np.tile(f_omega_vec, (len(t), 1))
        integrand = F_matrix * np.exp(1j * O * T)
        
        # Całkowanie po omega (rekonstrukcja)
        val = simpson(y=integrand, x=omega_vec, axis=1)
        
        # Wynik rzeczywisty skalowany przez 1/2pi
        res = val.real / (2 * np.pi)
        return res

    @staticmethod
    def trim_spectrum(omega_vec, f_omega_vec, k):
        """
        Przycina widmo do K najważniejszych współczynników (pod względem modułu).
        Reszta zostaje wyzerowana.
        """
        # Obliczamy moduły
        magnitudes = np.abs(f_omega_vec)
        
        # Znajdujemy indeksy K największych wartości
        idx_to_keep = np.argsort(magnitudes)[-k:]
        
        # Tworzymy nowe widmo (same zera) i przywracamy tylko K wybranych wartości
        f_trimmed = np.zeros_like(f_omega_vec, dtype=complex)
        f_trimmed[idx_to_keep] = f_omega_vec[idx_to_keep]
        
        return f_trimmed
    

class Fourier2:
    def __init__(self, t_vec, y_vec):
        """
        t_vec: wektor czasu (np. linspace)
        y_vec: wartości sygnału dla tych punktów czasu
        """
        self.t_vec = t_vec
        self.y_vec = y_vec

    def transform(self, omega):
        """
        Transformata prosta obliczana z tablicy danych.
        Obsługuje zarówno pojedyncze omega, jak i wektory numpy.
        omega: wektor częstotliwości
        """
        # Upewniamy się, że omega jest tablicą (nawet jeśli to jedna liczba)
        omega = np.atleast_1d(omega)
        
        exponent = -1j * omega[:, np.newaxis] * self.t_vec
        integrand = self.y_vec * np.exp(exponent)
        f_omega = simpson(y=integrand, x=self.t_vec, axis=1)
        
        # Jeśli na wejściu było jedno omega, zwróć skalar, w przeciwnym razie tablicę
        return f_omega if len(f_omega) > 1 else f_omega[0]

    def inverse_transform(self, omega_limit=15, num_omega=500):
        """Transformata odwrotna obliczana z widma
        t: wektor czasu
        omega_limit: granica częstotliwości 
        num_omega: ilość wykorzystanych częstotliwości
        """

        omega_vec = np.linspace(-omega_limit, omega_limit, num_omega)
        f_omega_vec = self.transform(omega_vec)
        
        t = np.atleast_1d(self.t_vec)
        T, O = np.meshgrid(t, omega_vec, indexing='ij')
        
        F_matrix = np.tile(f_omega_vec, (len(t), 1))
        integrand = F_matrix * np.exp(1j * O * T)
        
        val = simpson(y=integrand, x=omega_vec, axis=1)
        
        res = val.real / (2 * np.pi)
        return res if len(res) > 1 else res[0]
    
class DiscreteFourier:
    def __init__(self, t_vec, y_vec):
        """
        t_vec: wektor czasu (np. linspace)
        y_vec: wartości sygnału (musi być tej samej długości co t_vec)
        """
        self.t_vec = t_vec
        self.y_vec = y_vec
        self.N = len(t_vec)
        
        # Obliczamy krok czasu (dt) i częstotliwość próbkowania (fs)
        self.dt = t_vec[1] - t_vec[0]
        self.fs = 1.0 / self.dt

    def transform(self):
        """
        Oblicza Dyskretną Transformatę Fouriera (DFT).
        Zwraca: (freq_vec, f_k_vec)
        """
        # Generujemy indeksy k (częstotliwości) i n (czas)
        k = np.arange(self.N)
        n = np.arange(self.N)
        
        # Macierz wykładników dla DFT: exp(-j * 2pi * k * n / N)
        # Używamy meshgrid lub broadcasting dla szybkości
        K, N_idx = np.meshgrid(k, n, indexing='ij')
        W = np.exp(-2j * np.pi * K * N_idx / self.N)
        
        # Sumowanie (iloczyn macierzowy): F_k = suma(y_n * W_kn)
        f_k_vec = np.dot(W, self.y_vec)
        
        # Obliczamy wektor częstotliwości w Hz (standardowe dla DFT)
        freq_vec = k * (self.fs / self.N)
        
        return freq_vec, f_k_vec

    def inverse_transform(self, f_omega_vec):
        """
        Odtwarza sygnał na podstawie współczynników f_k_vec (IDFT).
        """
        N = len(f_omega_vec)
        k = np.arange(N)
        n = np.arange(N)
        
        # Macierz wykładników dla IDFT: exp(+j * 2pi * k * n / N)
        K, N_idx = np.meshgrid(k, n, indexing='ij')
        W_inv = np.exp(2j * np.pi * K * N_idx / N)
        
        # Sumowanie i skalowanie przez 1/N
        # n-ty element to suma po k
        res = np.dot(W_inv.T, f_omega_vec) / N
        
        return res.real

    @staticmethod
    def trim_spectrum(f_omega_vec, k):
        """
        Zeruje wszystkie współczynniki poza K największymi.
        """
        magnitudes = np.abs(f_omega_vec)
        # Znajdujemy próg dla k-tej największej wartości
        if k >= len(f_omega_vec):
            return f_omega_vec
            
        threshold_val = np.sort(magnitudes)[-k]
        
        f_trimmed = np.zeros_like(f_omega_vec, dtype=complex)
        mask = magnitudes >= threshold_val
        f_trimmed[mask] = f_omega_vec[mask]
        
        return f_trimmed