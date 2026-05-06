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
    