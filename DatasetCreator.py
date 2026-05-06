import numpy as np
from tqdm import tqdm
from SignalGenerator import APRBSSignal, MultisineSignal, FilteredNoiseSignal
from SignalData import SignalData


class DatasetCreator:
    def __init__(self, t_span=[0, 1000], dt=0.5, amp_range=(3, 9), noise_level=0.0):
        self.t_span = t_span
        self.dt = dt
        # Generujemy wektor czasu raz dla całego zestawu
        self.t_eval = np.arange(self.t_span[0], self.t_span[1], dt)
        self.amp_range = amp_range
        self.noise_level = noise_level

        # --- KONFIGURACJA ZAKRESÓW LOSOWANIA ---
        self.config = {
            "aprbs": {
                "h_min_range": (50, 150),
                "h_add_range": (100, 300)
            },
            "multisine": {
                "n_freqs_range": (5, 15),
                "f_max_range": (0.005, 0.02)
            },
            "noise": {
                "cutoff_range": (0.001, 0.01)
            }
        }

    def _get_signal_values(self, signal_type):
        """Tworzy obiekt sygnału i od razu zwraca wygenerowaną tablicę wartości."""
        sig_obj = None
        
        if signal_type == "aprbs":
            h_min = np.random.randint(*self.config["aprbs"]["h_min_range"])
            h_max = h_min + np.random.randint(*self.config["aprbs"]["h_add_range"])
            sig_obj = APRBSSignal(self.t_eval, self.amp_range, hold_range=(h_min, h_max))
            
        elif signal_type == "multisine":
            n_freqs = np.random.randint(*self.config["multisine"]["n_freqs_range"])
            f_max = np.random.uniform(*self.config["multisine"]["f_max_range"])
            sig_obj = MultisineSignal(self.t_eval, self.amp_range, n_freqs=n_freqs, f_max=f_max)
            
        elif signal_type == "noise":
            cutoff = np.random.uniform(*self.config["noise"]["cutoff_range"])
            sig_obj = FilteredNoiseSignal(self.t_eval, self.amp_range, cutoff=cutoff)
        
        # Zwracamy tablicę NumPy uzyskaną z metody generate()
        return sig_obj.generate() if sig_obj else None

    def _add_noise(self, signal_array):
        """Dodaje szum Gausowski do tablicy wartości."""
        noise = np.random.normal(0, self.noise_level, signal_array.shape)
        noisy_signal = signal_array + noise
        
        # Opcjonalnie: przycinanie do zakresu amp_range, żeby szum nie wykraczał poza fizykę
        return np.clip(noisy_signal, self.amp_range[0], self.amp_range[1])

    def _generate_category(self, n, signal_type):
        """Generuje listę tablic wartości dla konkretnej kategorii."""
        trajectories = []
        if n <= 0:
            return trajectories

        for _ in tqdm(range(n), desc=f"Generowanie {signal_type.upper()}"):
            # 1. Pobranie czystych wartości sygnału
            u_values = self._get_signal_values(signal_type)

            # 2. Ewentualne dodanie szumu do tablicy
            if self.noise_level > 0.0:
                u_values = self._add_noise(u_values)

            traj = SignalData(t=self.t_eval.copy(), y=u_values)
            trajectories.append(traj)    

        return trajectories

    def create_dataset(self, n_aprbs=10, n_multisine=10, n_noise=10):
        """
        Główna metoda zwracająca słownik z listami wygenerowanych sygnałów.
        """
        print(f"--- Start generowania zestawu danych (Noise Level: {self.noise_level}) ---")
        
        dataset = {
            "aprbs": self._generate_category(n_aprbs, "aprbs"),
            "multisine": self._generate_category(n_multisine, "multisine"),
            "noise": self._generate_category(n_noise, "noise")
        }

        print("\n--- Generowanie zakończone ---")
        for key, value in dataset.items():
            print(f"Kategoria {key.upper()}: {len(value)} sygnałów")
            
        return dataset