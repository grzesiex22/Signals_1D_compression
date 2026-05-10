'''
Tutaj możemy razem pisać kod do jupytera razem.
'''
import matplotlib
from matplotlib import pyplot as plt
from DatasetCreator import DatasetCreator
from Plotter import Plotter 
from Fourier import Fourier, Fourier2, DiscreteFourier
from EnergyAnalyzer import EnergyAnalyzer
from FidelityAnalyzer import FidelityAnalyzer
from Tester import FidelityTester
import numpy as np
# matplotlib.use('TkAgg') # %matplotlib widget

def main():
    tasks = {
        "Sygnały": generate_signals,
        "Fourier Dyskretny": discrete_fourier,
        "Fourier Nowy": new_fourier,
        "Fourier Stary": old_fourier,
        "Analiza Energii": analzize_energy,
        "Analiza Dokładości" : analyze_accuracy,
        "Testy": tests
    }

    # Wybierasz tylko te, które chcesz uruchomić
    active_tasks = ["Sygnały","Fourier Dyskretny", "Analiza Energii",
                    "Analiza Dokładości", "Testy"]

    for name in active_tasks:
        print(f"--- Uruchamiam: {name} ---")
        tasks[name]()

    return

def generate_signals():
    creator = DatasetCreator(t_span=[0, 500], dt=0.1, amp_range=(3, 90), noise_level=0.0)
    dataset = creator.create_dataset(n_aprbs=10, n_multisine=10, n_noise=10)

    for category, signals in dataset.items():
        print(f"\n=== Kategoria: {category.upper()} ===")
        for i, traj in enumerate(signals[:1]):  # Pokazujemy tylko 1 przykład
            print(f"Trajektoria nr {i+1}:")
            print(f"  t (pierwsze 5): {traj.t[:5]}")
            print(f"  y (pierwsze 5): {traj.y[:5]}")
            print(f"  Długość wektora: {len(traj.y)} próbek")
            print("-" * 30)

    # Rysowanie
    # Chcę porównać pierwszy, środkowy i ostatni sygnał ze wszystkich kategorii 
    Plotter.plot_indices(dataset['aprbs'], "aprbs", indices=[0, 5, 9])
    Plotter.plot_indices(dataset['multisine'], "multisine", indices=[0, 5, 9])
    Plotter.plot_indices(dataset['noise'], "noise", indices=[0, 5, 9])

def discrete_fourier():
    # 1. Generujemy dane
    creator = DatasetCreator(t_span=[0, 500], dt=0.1, amp_range=(3, 9), noise_level=0.0)
    dataset = creator.create_dataset(n_aprbs=10, n_multisine=10, n_noise=10)

    # sample_signal = dataset['aprbs'][0]  # Pobieramy pierwszy sygnał z kategorii APRBS
    sample_signal = dataset['multisine'][0]  # Pobieramy pierwszy sygnał z kategorii MULTISINE


    # 2. Inicjalizacja klasy Fourier
    fourier_engine = DiscreteFourier(sample_signal.t, sample_signal.y)

    k=100  # Liczba współczynników do zachowania (przycinanie)

    # 3. Obliczenie transformaty prostej dla zakresu częstotliwości
    omega_vec, f_omega_vec = fourier_engine.transform()
    print(f"Omega  (pierwsze 5): {f_omega_vec[:5]}")

    # 4. Przycinamy do 50 najważniejszych współczynników (K=50)
    f_trimmed = fourier_engine.trim_spectrum(f_omega_vec=f_omega_vec, k=k)

    # 4. Obliczenie transformaty odwrotnej (rekonstrukcja sygnału)
    y_reconstructed = fourier_engine.inverse_transform(f_trimmed)

    # 5. Wizualizacja wyników
    # Wykres widma (Część rzeczywista, urojona i moduł)
    Plotter.plot_fourier_transform(omega_vec, f_omega_vec, title="Widmo Fourier (Pełne)")
    Plotter.plot_fourier_transform(omega_vec, f_trimmed, title="Widmo Fourier (Przycięte do K=50)")

    # Wykres porównawczy (Oryginał vs Rekonstrukcja)
    Plotter.plot_fourier_comparison(
        sample_signal.t, 
        sample_signal.y, 
        y_reconstructed, 
        K=k,
        title=f"Rekonstrukcja dla analizy energii z FOURIER DYSKRETNY (K={k})"
    )

def new_fourier():
    # 1. Generujemy dane
    creator = DatasetCreator(t_span=[0, 500], dt=0.1, amp_range=(3, 9), noise_level=0.0)
    dataset = creator.create_dataset(n_aprbs=10, n_multisine=10, n_noise=10)

    # sample_signal = dataset['aprbs'][0]  # Pobieramy pierwszy sygnał z kategorii APRBS
    sample_signal = dataset['multisine'][0]  # Pobieramy pierwszy sygnał z kategorii MULTISINE


    # 2. Inicjalizacja klasy Fourier
    fourier_engine = Fourier(sample_signal.t, sample_signal.y)

    # Parametry analizy
    omega_limit = 5.0  # Zakres częstotliwości do analizy
    num_omega = 1000  # Liczba punktów w zakresie omega - Używamy mniejszego num_omega dla szybkości lub większego dla precyzji
    k=100  # Liczba współczynników do zachowania (przycinanie)

    print(f"--- Transformaty dla omega w zakresie [-{omega_limit}, {omega_limit}] ---")

    # 3. Obliczenie transformaty prostej dla zakresu częstotliwości
    omega_vec, f_omega_vec = fourier_engine.transform(omega_limit=omega_limit, num_omega=num_omega)
    print(f"Omega  (pierwsze 5): {f_omega_vec[:5]}")

    # 4. Przycinamy do 50 najważniejszych współczynników (K=50)
    f_trimmed = fourier_engine.trim_spectrum(omega_vec=omega_vec, f_omega_vec=f_omega_vec, k=k)

    # 4. Obliczenie transformaty odwrotnej (rekonstrukcja sygnału)
    y_reconstructed = fourier_engine.inverse_transform(omega_vec, f_trimmed)

    # 5. Wizualizacja wyników
    # Wykres widma (Część rzeczywista, urojona i moduł)
    Plotter.plot_fourier_transform(omega_vec, f_omega_vec, title="Widmo Fourier (Pełne)")
    Plotter.plot_fourier_transform(omega_vec, f_trimmed, title="Widmo Fourier (Przycięte do K=50)")

    # Wykres porównawczy (Oryginał vs Rekonstrukcja)
    Plotter.plot_fourier_comparison(
        sample_signal.t, 
        sample_signal.y, 
        y_reconstructed, 
        K=k,
        title=f"Rekonstrukcja dla analizy energii z FOURIER \n(Omega limit: {omega_limit}), (num_omega={num_omega}) (K={k})"
    )

def old_fourier():
    # 1. Generujemy dane
    creator = DatasetCreator(t_span=[0, 500], dt=0.1, amp_range=(3, 90), noise_level=0.0)
    dataset = creator.create_dataset(n_aprbs=10, n_multisine=10, n_noise=10)

    sample_signal = dataset['multisine'][0]  # Pobieramy pierwszy sygnał z kategorii MULTISINE

    # 2. Inicjalizacja klasy Fourier
    fourier_engine = Fourier2(sample_signal.t, sample_signal.y)

    # 3. Obliczenie transformaty prostej dla zakresu częstotliwości
    omega_limit = 5.0  # Zakres częstotliwości do analizy
    omega_vec = np.linspace(-omega_limit, omega_limit, 500)
    f_omega = fourier_engine.transform(omega_vec)

    print(f"--- Transformaty dla omega w zakresie [-{omega_limit}, {omega_limit}] ---")
    print(f"Omega  (pierwsze 5): {f_omega[:5]}")

    # 4. Obliczenie transformaty odwrotnej (rekonstrukcja sygnału)
    # Używamy mniejszego num_omega dla szybkości lub większego dla precyzji
    y_reconstructed = fourier_engine.inverse_transform(
        omega_limit=omega_limit, 
        num_omega=1000
    )

    # 5. Wizualizacja wyników
    # Wykres widma (Część rzeczywista, urojona i moduł)
    Plotter.plot_fourier_transform(omega_vec, f_omega)

    # Wykres porównawczy (Oryginał vs Rekonstrukcja)
    Plotter.plot_fourier_comparison(
        sample_signal.t, 
        sample_signal.y, 
        y_reconstructed, 
        K=0,
        title=f"Rekonstrukcja dla analizy energii z FOURIER 2 (Omega limit: {omega_limit})"
    )

def analzize_energy():
    # 1. Generujemy dane
    creator = DatasetCreator(t_span=[0, 500], dt=0.1, amp_range=(3, 90), noise_level=0.0)
    dataset = creator.create_dataset(n_aprbs=10, n_multisine=10, n_noise=10)

    energy_threshold = 0.999  # Procent energii do zachowania (np. 0.999 dla 99.9%)

    # 2. Analiza energii dla NUMPY FFT
    print("\n--- ANALIZA SYGNAŁU MULTISINE - NUMPY FFT ---")# Pobieramy pierwszy sygnał z listy
    signal = dataset['multisine'][0] 

    # 2.1. Analiza energii w dziedzinie czasu
    e_time = EnergyAnalyzer.calculate_total_energy(signal)
    print(f"Energia w dziedzinie czasu: {e_time:.2f}")

    # 2.2. Analiza energii w dziedzinie częstotliwości (FFT)
    coeffs = np.fft.rfft(signal.y)
    # Częstotliwości odpowiadające współczynnikom (w Hz lub rad/s)
    freqs = np.fft.rfftfreq(len(signal.y), d=(signal.t[1] - signal.t[0]))
    omega_numpy = 2 * np.pi * freqs

    results = EnergyAnalyzer.analyze_energy_distribution(coeffs, N=len(signal.y), threshold=energy_threshold)
    print(f"Wspołczynniki FFT - liczba: {len(coeffs)}...")  # Pokazujemy tylko pierwsze 5 współczynników
    print(f"Wspołczynniki FFT: {coeffs[:5]}...")  # Pokazujemy tylko pierwsze 5 współczynników
    print(f"Energia w dziedzinie częstotliwości: {results['total_energy_freq']:.2f}")
    print(f"Liczba współczynników (K) dla {energy_threshold*100}% energii: {results['k_threshold']}")

    # 2.3. Przycinanie widma (metoda analogiczna do trim_spectrum)
    # Sortujemy po amplitudzie i zostawiamy tylko K największych, reszta -> 0
    magnitudes = np.abs(coeffs)
    # Pobieramy próg wartości dla k-tego największego elementu
    threshold_val = np.sort(magnitudes)[-results['k_threshold']]
    coeffs_trimmed = np.where(magnitudes >= threshold_val, coeffs, 0)

    # 2.4. Transformata odwrotna (Inverse Real FFT)
    # irfft automatycznie odtwarza sygnał o długości N na podstawie współczynników rfft
    y_reconstructed_np = np.fft.irfft(coeffs_trimmed, n=len(signal.y))

    # 2.5. Wizualizacja wyników
    # Wykres widma (Część rzeczywista, urojona i moduł)
    Plotter.plot_fourier_transform(omega_numpy, coeffs, title="Widmo Fourier (Pełne) - np.fft.rfft")
    Plotter.plot_fourier_transform(omega_numpy, coeffs_trimmed, title="Widmo obliczone przez np.fft.rfft")

    # Wykres porównawczy (Oryginał vs Rekonstrukcja)
    # Rysujesz wynik
    Plotter.plot_fourier_comparison(
        signal.t, 
        signal.y, 
        y_reconstructed_np, 
        K=results['k_threshold'],
        title=f"Rekonstrukcja dla analizy energii z transformatą np.fft"
    )

    # 3. Analiza energii dla WŁASNEGO FFT
    print("\n--- ANALIZA SYGNAŁU MULTISINE - WŁASNA FFT ---")# Pobieramy pierwszy sygnał z listy
    signal = dataset['multisine'][0] 

    # 3.1. Analiza energii w dziedzinie czasu
    e_time = EnergyAnalyzer.calculate_total_energy(signal)
    print(f"Energia w dziedzinie czasu: {e_time:.2f}")

    # 3.2. Analiza energii w dziedzinie częstotliwości (FFT)
    fourier_engine = DiscreteFourier(signal.t, signal.y)
    frq, cfs = fourier_engine.transform()

    results_dsc = EnergyAnalyzer.analyze_energy_distribution(cfs, N=len(signal.y), threshold=energy_threshold)
    print(f"Wspołczynniki FFT - liczba: {len(coeffs)}...")  # Pokazujemy tylko pierwsze 5 współczynników
    print(f"Wspołczynniki FFT: {coeffs[:5]}...")  # Pokazujemy tylko pierwsze 5 współczynników
    print(f"Energia w dziedzinie częstotliwości: {results_dsc['total_energy_freq']:.2f}")
    print(f"Liczba współczynników (K) dla {energy_threshold*100}% energii: {results_dsc['k_threshold']}")

    # 3.3. Obliczenie transformaty prostej dla zakresu częstotliwości
    omega_vec, f_omega_vec = fourier_engine.transform()

    # 3.4. Przycinamy do 50 najważniejszych współczynników (K=50)
    f_trimmed = fourier_engine.trim_spectrum(f_omega_vec=f_omega_vec, k=results_dsc['k_threshold'])

    # 3.5. Obliczenie transformaty odwrotnej (rekonstrukcja sygnału)
    y_reconstructed = fourier_engine.inverse_transform(f_trimmed)

    # 3.6. Wizualizacja wyników
    # Wykres widma (Część rzeczywista, urojona i moduł)
    Plotter.plot_fourier_transform(omega_vec, f_omega_vec, title="Widmo Fourier (Pełne)")
    Plotter.plot_fourier_transform(omega_vec, f_trimmed, title=f"Widmo Fourier (Przycięte do K={results_dsc['k_threshold']})")

    # Wykres porównawczy (Oryginał vs Rekonstrukcja)
    Plotter.plot_fourier_comparison(
        signal.t, 
        signal.y, 
        y_reconstructed, 
        K=results_dsc['k_threshold'],
        title=f"Rekonstrukcja dla analizy energii z transformatą własną implementacją"
    )

def analyze_accuracy():
    # 1. Generujemy dane
    creator = DatasetCreator(t_span=[0, 500], dt=0.1, amp_range=(3, 90), noise_level=0.0)
    dataset = creator.create_dataset(n_aprbs=10, n_multisine=10, n_noise=10)

    print("\n--- ANALIZA SYGNAŁU MULTISINE ---")# Pobieramy pierwszy sygnał z listy
    signal = dataset['multisine'][0] 

    # 1. Obliczasz FFT za pomocą numpy
    coeffs = np.fft.rfft(signal.y)

    # 2. Szukasz K dla Max Error = 2.0 (czyli niebieska linia ma być b. blisko czerwonej)
    # Ustaw próg dopasowany do Twojej amp_range (np. 3-5% amplitudy sygnału)
    max_allowed_diff = 2.0 
    mode = 'mse'  # Możesz też użyć 'max_error' jeśli chcesz sprawdzać maksymalny błąd zamiast MSE
    results = FidelityAnalyzer.analyze_by_error(signal.y, coeffs, threshold=max_allowed_diff, mode=mode)

    print(f"Aby błąd maksymalny był < {max_allowed_diff}, potrzeba K = {results['k_threshold']}")

    # 3. Rysujesz wynik
    Plotter.plot_fourier_comparison(
        signal.t, 
        signal.y, 
        results['reconstructed_y'], 
        K=results['k_threshold'],
        title=f"Rekonstrukcja dla {mode.upper()} < {max_allowed_diff}"
    )

def tests():
    # 1. Generujemy duży zbiór (np. po 50-100 sygnałów na klase)
    creator = DatasetCreator(t_span=[0, 500], dt=0.1, amp_range=(3, 90), noise_level=0.0)
    big_dataset = creator.create_dataset(n_aprbs=100, n_multisine=100, n_noise=100)

    # 2. Inicjalizujemy testera
    tester = FidelityTester(big_dataset)

    # 3. Puszczamy testy (np. chcemy błąd maksymalny nie większy niż 3 jednostki)
    stats = tester.run(threshold=3.0, mode='max')

    # 4. Wyświetlamy raport
    print("--- RAPORT KOSZTU REPREZENTACJI (K) ---")
    print(tester.display_results())


if __name__ == "__main__":
    main()
