import matplotlib.pyplot as plt
import numpy as np


class Plotter:
    @staticmethod
    def plot_single(signal_data, title="Sygnał", color='b'):
        """Rysuje pojedynczy sygnał."""
        plt.figure(figsize=(8, 3))
        plt.plot(signal_data.t, signal_data.y, color=color, linewidth=1.5)
        plt.title(title)
        plt.xlabel("Czas [s]")
        plt.ylabel("Amplituda [V]")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_category(signals, category_name, n=3):
        """Rysuje kilka (n) sygnałów z danej kategorii na jednym wykresie (jeden pod drugim)."""
        n = min(n, len(signals))
        fig, axes = plt.subplots(n, 1, figsize=(8, 2 * n), sharex=True)
        
        if n == 1: axes = [axes] # Obsługa przypadku, gdy n=1

        colors = {'aprbs': 'red', 'multisine': 'blue', 'noise': 'green'}
        color = colors.get(category_name.lower(), 'black')

        for i in range(n):
            axes[i].plot(signals[i].t, signals[i].y, color=color)
            axes[i].set_ylabel("Amp [V]")
            axes[i].grid(True, alpha=0.3)
            if i == 0:
                axes[i].set_title(f"Próbki sygnałów z kategorii: {category_name.upper()}")

        axes[-1].set_xlabel("Czas [s]")
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_indices(signals, category_name, indices=[0]):
        """
        Rysuje sygnały o konkretnych indeksach z danej kategorii.
        
        Args:
            signals (list): Lista obiektów SignalData.
            category_name (str): Nazwa kategorii (do tytułu i koloru).
            indices (list): Lista indeksów, np. [0, 10, 99].
        """
        # Sprawdzamy, czy indeksy mieszczą się w liście
        valid_indices = [i for i in indices if i < len(signals)]
        num_plots = len(valid_indices)
        
        if num_plots == 0:
            print("Błąd: Podane indeksy są poza zakresem danych.")
            return

        fig, axes = plt.subplots(num_plots, 1, figsize=(8, 2 * num_plots), sharex=True)
        
        # Jeśli rysujemy tylko jeden sygnał, matplotlib nie zwraca listy osi
        if num_plots == 1:
            axes = [axes]

        # Konfiguracja wizualna
        colors = {'aprbs': '#e74c3c', 'multisine': '#3498db', 'noise': '#27ae60'}
        color = colors.get(category_name.lower(), 'black')

        for i, idx in enumerate(valid_indices):
            sig = signals[idx]
            axes[i].plot(sig.t, sig.y, color=color, linewidth=1.2)
            axes[i].set_ylabel(f"Indeks: {idx}\nY")
            axes[i].grid(True, alpha=0.3)
            
            if i == 0:
                axes[i].set_title(f"Analiza wybranych próbek: {category_name.upper()}")

        axes[-1].set_xlabel("Czas [s]")
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_fourier_transform(omega_values, fourier_values, title="Analiza Transformaty Fouriera"):
        # Inicjalizacja figury z odpowiednim rozmiarem (szerokość, wysokość)
        plt.figure(figsize=(8, 6.5))

        # Dodanie tytułu ogólnego dla całej figury
        plt.suptitle(title, fontsize=16, fontweight='bold', y=0.98)

        # Wykres części rzeczywistej
        plt.subplot(3, 1, 1)
        plt.plot(omega_values, fourier_values.real, label=r"Re$\{\hat{f}(\omega)\}$", color='blue')
        plt.title("Część rzeczywista transformaty Fouriera", fontsize=14)
        plt.xlabel(r"$\omega$", fontsize=12)
        plt.ylabel(r"Re$\{\hat{f}(\omega)\}$", fontsize=12)
        plt.grid(True)

        # Wykres części urojonej
        plt.subplot(3, 1, 2)
        plt.plot(omega_values, fourier_values.imag, label=r"Im$\{\hat{f}(\omega)\}$", color='red')
        plt.title("Część urojona transformaty Fouriera", fontsize=14)
        plt.xlabel(r"$\omega$", fontsize=12)
        plt.ylabel(r"Im$\{\hat{f}(\omega)\}$", fontsize=12)
        plt.grid(True)

        # Wykres modułu |F(ω)|
        plt.subplot(3, 1, 3)
        plt.plot(omega_values, np.abs(fourier_values), label=r"$|\hat{f}(\omega)|$", color='green')
        plt.title("Moduł transformaty Fouriera", fontsize=14)
        plt.xlabel(r"$\omega$", fontsize=12)
        plt.ylabel(r"$|\hat{f}(\omega)|$", fontsize=12)
        plt.grid(True)

        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_fourier_comparison(t_data, y_original, y_approx, K, title="Porównanie sygnału oryginalnego z rekonstrukcją z widma"):
        plt.figure(figsize=(8, 4))
        plt.plot(t_data, y_original, 'r-', linewidth=2, label='Oryginalny sygnał (Impuls)')
        plt.plot(t_data, y_approx, 'b--', alpha=0.6, label=f'Przybliżenie (Odwrotny Fourier, K={K})')

        plt.title(title, fontsize=16)
        plt.xlabel("Czas (t)", fontsize=14)
        plt.ylabel("Amplituda", fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.show()

    @staticmethod
    def plot_fourier_histogram(fourier_obj, omega_limit=10, num_prążków=21):
        """
        Rysuje histogram (wykres prążkowy) składowych cosinusowych i sinusowych.
        
        fourier_obj: instancja klasy Fourier
        omega_limit: maksymalna częstotliwość na wykresie
        num_prążków: ile słupków chcemy wyświetlić 
        """
        # 1. Wyznaczenie dyskretnych częstotliwości (omega)
        omegas = np.linspace(-omega_limit, omega_limit, num_prążków)
        
        # 2. Obliczenie wartości transformaty dla tych omeg
        # Zakładamy, że Twoja metoda transform obsługuje wektory
        spectrum = fourier_obj.transform(omegas)
        
        cos_parts = spectrum.real
        sin_parts = spectrum.imag

        # 3. Tworzenie wykresu
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
        
        # Wykres dla cosinusów (Część rzeczywista)
        ax1.bar(omegas, cos_parts, color='royalblue', alpha=0.7, width=0.3, label='Re (Kosinusy)')
        ax1.axhline(0, color='black', lw=1)
        ax1.set_ylabel('Amplituda Re')
        ax1.set_title('Histogram składowych kosinusowych')
        ax1.grid(True, axis='y', linestyle='--', alpha=0.7)
        ax1.legend()

        # Wykres dla Sinusów (Część urojona)
        ax2.bar(omegas, sin_parts, color='crimson', alpha=0.7, width=0.3, label='Im (Sinusy)')
        ax2.axhline(0, color='black', lw=1)
        ax2.set_ylabel('Amplituda Im')
        ax2.set_xlabel(r'Częstotliwość ($\omega$)')
        ax2.set_title('Histogram składowych sinusowych')
        ax2.grid(True, axis='y', linestyle='--', alpha=0.7)
        ax2.legend()

        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_k_histogram(k, title="Histogram współczynników Fouriera"):
        plt.figure(figsize=(8, 4))
        plt.hist(k, 
                bins=20,             
                color='royalblue',    
                edgecolor='black',    
                alpha=0.7,            
                rwidth=0.85)
        
        plt.title(title, fontsize=16)
        plt.xlabel("Współczynniki Fouriera", fontsize=14)
        plt.ylabel("Ilość wykorzystanych współczynników", fontsize=14)
        plt.grid(axis='y', linestyle='--', alpha=0.4)
        plt.show()