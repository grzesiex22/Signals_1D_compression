import numpy as np
from tqdm.notebook import tqdm
from SignalGenerator import APRBSSignal, MultisineSignal, FilteredNoiseSignal
from SignalData import SignalData
import copy

class DatasetCreator:
    def __init__(self, t_span=[0, 1000], dt=0.5, amp_range=(3, 9), noise_level=0.0, seed=None, verbose=False):
        self.t_span = t_span
        self.dt = dt
        # Generujemy wektor czasu raz dla całego zestawu
        self.t_eval = np.arange(self.t_span[0], self.t_span[1], dt)
        self.amp_range = amp_range
        self.verbose = verbose
        self.noise_level = noise_level
        self.dataset = None
        
        # Inicjalizacja nowego, bezpiecznego generatora liczb losowych NumPy
        self.rng = np.random.default_rng(seed)

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
        
        # UWAGA: Aby zachować powtarzalność, Twoje klasy (APRBSSignal itd.) 
        # powinny przyjmować obiekt self.rng i używać go wewnętrznie do losowania!
        if signal_type == "aprbs":
            h_min = self.rng.integers(*self.config["aprbs"]["h_min_range"])
            h_max = h_min + self.rng.integers(*self.config["aprbs"]["h_add_range"])
            sig_obj = APRBSSignal(self.t_eval, self.amp_range, hold_range=(h_min, h_max), rng=self.rng)
            
        elif signal_type == "multisine":
            n_freqs = self.rng.integers(*self.config["multisine"]["n_freqs_range"])
            f_max = self.rng.uniform(*self.config["multisine"]["f_max_range"])
            sig_obj = MultisineSignal(self.t_eval, self.amp_range, n_freqs=n_freqs, f_max=f_max, rng=self.rng)
            
        elif signal_type == "noise":
            cutoff = self.rng.uniform(*self.config["noise"]["cutoff_range"])
            sig_obj = FilteredNoiseSignal(self.t_eval, self.amp_range, cutoff=cutoff, rng=self.rng)
        
        # Zwracamy tablicę NumPy uzyskaną z metody generate()
        return sig_obj.generate() if sig_obj else None

    def _add_noise(self, signal_array):
        """Dodaje szum Gausowski do tablicy wartości przy użyciu generatora stanów."""
        noise = self.rng.normal(0, self.noise_level, signal_array.shape)
        noisy_signal = signal_array + noise
        
        # Opcjonalnie: przycinanie do zakresu amp_range, żeby szum nie wykraczał poza fizykę
        return np.clip(noisy_signal, self.amp_range[0], self.amp_range[1])

    def _generate_category(self, n, signal_type):
        """Generuje listę tablic wartości dla konkretnej kategorii."""
        trajectories = []
        if n <= 0:
            return trajectories

        for _ in tqdm(range(n), desc=f"Generowanie {signal_type.upper()}"):
            # Pobranie czystych wartości sygnału
            u_values = self._get_signal_values(signal_type)

            traj = SignalData(t=self.t_eval.copy(), y=u_values)
            trajectories.append(traj)    

        return trajectories

    def create_dataset(self, n_aprbs=10, n_multisine=10, n_noise=10):
        """
        Główna metoda zwracająca słownik z listami wygenerowanych sygnałów.
        """
        
        if self.verbose:
            print(f"--- Generowanie datasetu ---")
        
        self.dataset = {
            "aprbs": self._generate_category(n_aprbs, "aprbs"),
            "multisine": self._generate_category(n_multisine, "multisine"),
            "noise": self._generate_category(n_noise, "noise")
        }

        if self.verbose:
            print("\n--- Generowanie zakończone ---")
            for key, value in self.dataset.items():
                print(f"Kategoria {key.upper()}: {len(value)} sygnałów")
            
        return self.dataset
    
    def create_noisy_dataset_copy(self):
        """
        Tworzy głęboką kopię istniejącego datasetu zapisanego w instancji i dodaje szum Gaussowski.
            
        Returns:
            dict: Nowy słownik z zaszumionymi kopiami sygnałów (oryginał w self.dataset pozostaje czysty).
        """
        
        # Bezpiecznik: Sprawdzenie, czy użytkownik najpierw wywołał create_dataset()
        if self.dataset is None:
            raise ValueError("Najpierw musisz wygenerować dataset za pomocą metody .create_dataset()!")
            
        # Głęboka kopiowanie całej struktury
        noisy_dataset = copy.deepcopy(self.dataset)
        
        if self.verbose:
            print(f"--- Generowanie zaszumionej kopii (Noise Level: {self.noise_level}) ---")
        
        # Iteracja po kategoriach i obiektach SignalData
        for category, signal_list in noisy_dataset.items():
            for signal_obj in signal_list:
                # Generowanie szumu przy użyciu stanów wbudowanego generatora self.rng
                noise = self.rng.normal(0, self.noise_level, signal_obj.y.shape)
                
                # Dodanie szumu do skopiowanych wartości
                noisy_y = signal_obj.y + noise
                
                # Przycięcie wartości do barier zdefiniowanych w konstruktorze klasy
                signal_obj.y = np.clip(noisy_y, self.amp_range[0], self.amp_range[1])

        if self.verbose:        
            print("--- Kopiowanie i zaszumianie zakończone ---")
            
        return noisy_dataset