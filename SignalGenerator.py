import numpy as np
from matplotlib import pyplot as plt


class BaseSignal:
    """
    Klasa bazowa dla generatorów sygnałów pobudzających.
    Definiuje podstawowe parametry czasowe i zakresy amplitud.
    """
    def __init__(self, t_eval, amp_range=(2, 8)):
        """
        Inicjalizacja parametrów sygnału.

        Args:
            t_eval (float): Wektor czasu [s].
            amp_range (tuple): Zakres dopuszczalnych napięć (min, max) [V].
        """
        self.t = t_eval
        self.amin, self.amax = amp_range
        self.dt = t_eval[1] - t_eval[0] if len(t_eval) > 1 else 0


class APRBSSignal(BaseSignal):
    def __init__(self, t_eval, amp_range=(2, 8), hold_range=(50, 200)):
        super().__init__(t_eval, amp_range)
        self.hold_range = hold_range

    def generate(self):
        """Generuje ciąg wartości skokowych."""
        u = np.zeros_like(self.t)
        i = 0
        while i < len(self.t):
            hold = np.random.randint(*self.hold_range)
            amplitude = np.random.uniform(self.amin, self.amax)
            u[i : i + hold] = amplitude
            i += hold
        return u[:len(self.t)]


class MultisineSignal(BaseSignal):
    def __init__(self, t_eval, amp_range=(2, 8), n_freqs=10, f_max=0.02):
        super().__init__(t_eval, amp_range)
        self.n_freqs = n_freqs
        self.f_max = f_max

    def generate(self):
        """Generuje sumę sinusów znormalizowaną do zakresu."""
        freqs = np.random.uniform(0.00001, self.f_max, self.n_freqs)
        phases = np.random.uniform(0, 2 * np.pi, self.n_freqs)
        
        # Szybka operacja na wektorze czasu
        u_raw = np.zeros_like(self.t)
        for f, p in zip(freqs, phases):
            u_raw += np.sin(2 * np.pi * f * self.t + p)

        # Normalizacja do [0, 1] i skalowanie do [amin, amax]
        u_norm = (u_raw + self.n_freqs) / (2 * self.n_freqs)
        return u_norm * (self.amax - self.amin) + self.amin


class FilteredNoiseSignal(BaseSignal):
    def __init__(self, t_eval, amp_range=(2, 8), cutoff=0.001):
        super().__init__(t_eval, amp_range)
        self.cutoff = cutoff

    def generate(self):
        """Generuje przefiltrowany szum znormalizowany do zakresu."""
        noise = np.random.randn(len(self.t))
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


# Generowanie próbek
# gen1 = APRBSSignal(t_end=1000, dt=0.5, amp_range=(3, 9))
# u_aprbs = gen1.generate()
# gen2 = MultisineSignal(t_end=1000, dt=0.5, amp_range=(3, 9))
# u_sine = gen2.generate()
# gen3 = FilteredNoiseSignal(t_end=1000, dt=0.5, amp_range=(3, 9))
# u_noise = gen3.generate()


# # Wykresy
# plt.figure(figsize=(12, 8))

# plt.subplot(3, 1, 1)
# plt.step(gen1.t, u_aprbs, 'r', where='post')
# plt.title("APRBS (Skoki napięcia - uczy stanów ustalonych)")
# plt.grid(True, alpha=0.3)

# plt.subplot(3, 1, 2)
# plt.plot(gen2.t, u_sine, 'b')
# plt.title("Multisine (Gładkie fale - uczy dynamiki częstotliwościowej)")
# plt.grid(True, alpha=0.3)

# plt.subplot(3, 1, 3)
# plt.plot(gen3.t, u_noise, 'g')
# plt.title("Filtered Noise (Szum - uczy odporności na chaos)")
# plt.xlabel("Czas [s]")
# plt.grid(True, alpha=0.3)

# plt.tight_layout()
# plt.show()