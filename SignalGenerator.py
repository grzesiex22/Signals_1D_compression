import numpy as np
from matplotlib import pyplot as plt


class BaseSignal:
    """
    Klasa bazowa dla generatorów sygnałów pobudzających.
    Definiuje podstawowe parametry czasowe, zakresy amplitud oraz generator stanów losowych.
    """
    def __init__(self, t_eval, amp_range=(2, 8), rng=None):
        """
        Inicjalizacja parametrów sygnału.

        Args:
            t_eval (np.ndarray): Wektor czasu [s].
            amp_range (tuple): Zakres dopuszczalnych napięć (min, max) [V].
            rng (np.random.Generator, optional): Instancja generatora liczb losowych.
        """
        self.t = t_eval
        self.amin, self.amax = amp_range
        self.dt = t_eval[1] - t_eval[0] if len(t_eval) > 1 else 0
        
        # Przypisanie przekazanego generatora lub utworzenie nowego (w przypadku braku seeda)
        self.rng = rng if rng is not None else np.random.default_rng()


class APRBSSignal(BaseSignal):
    def __init__(self, t_eval, amp_range=(2, 8), hold_range=(50, 200), rng=None):
        super().__init__(t_eval, amp_range, rng=rng)
        self.hold_range = hold_range

    def generate(self):
        """Generuje ciąg wartości skokowych z zachowaniem powtarzalności."""
        u = np.zeros_like(self.t)
        i = 0
        while i < len(self.t):
            # Podmiana np.random.randint -> self.rng.integers
            hold = self.rng.integers(*self.hold_range)
            amplitude = self.rng.uniform(self.amin, self.amax)
            u[i : i + hold] = amplitude
            i += hold
        return u[:len(self.t)]


class MultisineSignal(BaseSignal):
    def __init__(self, t_eval, amp_range=(2, 8), n_freqs=10, f_max=0.02, rng=None):
        super().__init__(t_eval, amp_range, rng=rng)
        self.n_freqs = n_freqs
        self.f_max = f_max

    def generate(self):
        """Generuje sumę sinusów znormalizowaną do zakresu z zachowaniem powtarzalności."""
        freqs = self.rng.uniform(0.00001, self.f_max, self.n_freqs)
        phases = self.rng.uniform(0, 2 * np.pi, self.n_freqs)
        
        # Szybka operacja na wektorze czasu
        u_raw = np.zeros_like(self.t)
        for f, p in zip(freqs, phases):
            u_raw += np.sin(2 * np.pi * f * self.t + p)

        # Normalizacja do [0, 1] i skalowanie do [amin, amax]
        u_norm = (u_raw + self.n_freqs) / (2 * self.n_freqs)
        return u_norm * (self.amax - self.amin) + self.amin


class FilteredNoiseSignal(BaseSignal):
    def __init__(self, t_eval, amp_range=(2, 8), cutoff=0.001, rng=None):
        super().__init__(t_eval, amp_range, rng=rng)
        self.cutoff = cutoff

    def generate(self):
        """Generuje przefiltrowany szum znormalizowany do zakresu z zachowaniem powtarzalności."""
        # Podmiana np.random.randn -> self.rng.standard_normal
        noise = self.rng.standard_normal(len(self.t))
        u = np.zeros_like(noise)
        
        # Współczynnik filtra dolnoprzepustowego
        alpha = (2 * np.pi * self.cutoff * self.dt) / (2 * np.pi * self.cutoff * self.dt + 1)

        for i in range(1, len(noise)):
            u[i] = u[i - 1] + alpha * (noise[i] - u[i - 1])

        u_min, u_max = u.min(), u.max()
        if abs(u_max - u_min) < 1e-9:
            return np.full_like(u, self.amin)

        u_norm = (u - u_min) / (u_max - u_min)
        return u_norm * (self.amax - self.amin) + self.amin