import numpy as np
import pandas as pd 
import os   
from tqdm.notebook import tqdm  # Paski postępu dla Jupyter Notebook
from Fourier import DiscreteFourier
from FidelityAnalyzer import FidelityAnalyzer
from FidelityAnalyzer import EnergyAnalyzer 
from SignalMetrics import SignalMetrics
from TableRenderer import ReportTableRenderer

class TesterUtils:
    @staticmethod
    def save_csv(data, folder, filename):
        """
        Zapisuje surowe lub zagregowane dane do pliku CSV w folderze Results.
        """
        # 1. Najpierw bezpiecznie sprawdzamy DataFrame (metodą dedykowaną .empty)
        if isinstance(data, pd.DataFrame):
            if data.empty:
                print("[INFO] Brak danych (pusta ramka DataFrame) do zapisu CSV.")
                return
        # 2. Jeśli to nie DataFrame, a zwykła lista/słownik - sprawdzamy standardowo
        elif not data:
            print("[INFO] Brak danych (pusta lista) do zapisu CSV.")
            return

        # Dalsza część funkcji pozostaje bez zmian...
        output_dir = f"Results\\{folder}"
        os.makedirs(output_dir, exist_ok=True)
        full_path = os.path.join(output_dir, filename)
        
        df = pd.DataFrame(data) if isinstance(data, list) else data.copy()
            
        if 'PRD' in df.columns:
            df['PRD'] = df['PRD'].apply(lambda x: float(str(x).replace('%', '')) if pd.notnull(x) else 0.0)
            
        df.to_csv(full_path, index=False, sep=';', encoding='utf-8')
        print(f"[ZAPIS CSV] Dane pomyślnie zapisano w: {full_path}")

    @staticmethod
    def aggregate(raw_results):
        """
        Przyjmuje surową listę słowników i zwraca zagregowany obiekt DataFrame ze statystykami.
        args:
            raw_results (list): Surowa lista słowników z wynikami testów dla każdego sygnału i progu dokładności
        returns:    
            pd.DataFrame: Zagregowany DataFrame z obliczonymi statystykami dla każdej kombinacji strategii i konfiguracji
        """
        if not raw_results:
            return pd.DataFrame()

        df = pd.DataFrame(raw_results)
        if df['PRD'].dtype == object:
            df['PRD'] = df['PRD'].str.replace('%', '').astype(float)

        summary = df.groupby(["Strategia", "Konfiguracja"]).agg( 
            count=('Wymagane K', 'size'), # <-- Dodana liczba elementów w grupie (N)           
            mean_K=('Wymagane K', 'mean'), min_K=('Wymagane K', 'min'),
            max_K=('Wymagane K', 'max'), std_K=('Wymagane K', 'std'),
            mean_MSE=('MSE', 'mean'), mean_RMSE=('RMSE', 'mean'),
            mean_MaxError=('Max Error', 'mean'), mean_PRD=('PRD', 'mean')
        ).reset_index().fillna(0.0)
        return summary

    @staticmethod
    def render(category_name, summary_df, save_md=True, save_name_suffix=None, folder="Default"):
        """
        Uniwersalny generator tabel raportowych. Automatycznie rozpoznaje kryterium
        (Energetyczne/Fidelity) na podstawie danych w DataFrame, dobiera precyzję i tworzy pliki .md.
        """
        if summary_df.empty:
            print("[INFO] Brak danych do wyrenderowania tabeli.")
            return

        output_dir = f"Results\\{folder}"
        os.makedirs(output_dir, exist_ok=True)

        # Dynamiczne wykrywanie strategii na podstawie zawartości ramki danych
        strategy_sample = str(summary_df['Strategia'].iloc[0]).lower()
        
        if "energetyczne" in strategy_sample:
            criterion_label = "Kryterium Energetyczne"
            file_label = "energy"
        elif "mse" in strategy_sample:
            criterion_label = "Kryterium Dokładnościowe (Fidelity MSE)"
            file_label = "fidelity_mse"
        else:
            criterion_label = "Kryterium Dokładnościowe (Fidelity Max Error)"
            file_label = "fidelity_max_error"

        title = f"{criterion_label} - Zbiorczy raport dla sygnałów: {category_name.upper()}"
        headers = ["Strategia", "Konfiguracja", "Liczba sygnałów", "Średnie K", "Min K", "Max K", "Std(K)", "Średnie MSE", "Średnie RMSE", "Średni Max Error", "Średni PRD"]
        
        # Matematyczne wyznaczanie optymalnej liczby miejsc po przecinku w kolumnie
        def get_precision_format(series, default_decimals=2):
            non_zeros = series[series > 0]
            if non_zeros.empty: return f"{{:.{default_decimals}f}}"
            min_val = non_zeros.min()
            if min_val < 1:
                first_significant_digit_pos = int(np.floor(np.log10(min_val)))
                decimals = max(default_decimals, -first_significant_digit_pos + 2)
                return f"{{:.{decimals}f}}"
            return f"{{:.{default_decimals}f}}"

        fmt_mean_K = get_precision_format(summary_df['mean_K'], default_decimals=1)
        fmt_std_K  = get_precision_format(summary_df['std_K'], default_decimals=2)
        fmt_MSE    = get_precision_format(summary_df['mean_MSE'], default_decimals=2)
        fmt_RMSE   = get_precision_format(summary_df['mean_RMSE'], default_decimals=2)
        fmt_MaxErr = get_precision_format(summary_df['mean_MaxError'], default_decimals=2)
        fmt_PRD    = get_precision_format(summary_df['mean_PRD'], default_decimals=2)

        rows = []
        for _, r in summary_df.iterrows():
            rows.append([
                str(r['Strategia']), str(r['Konfiguracja']),
                str(int(r['count'])),
                fmt_mean_K.format(r['mean_K']), str(int(r['min_K'])), str(int(r['max_K'])),
                fmt_std_K.format(r['std_K']), fmt_MSE.format(r['mean_MSE']), fmt_RMSE.format(r['mean_RMSE']),
                fmt_MaxErr.format(r['mean_MaxError']), f"{fmt_PRD.format(r['mean_PRD'])}%"
            ])
            
        # # Generowanie pliku Markdown
        # if save_md:
        #     if not save_name_suffix:
        #         save_name_suffix = f"default_name_table_{file_label}_{category_name.lower()}"
        #     formatted_df = pd.DataFrame(rows, columns=headers)
        #     md_filename = os.path.join(output_dir, f"{save_name_suffix}.md")
        #     with open(md_filename, "w", encoding="utf-8") as f:
        #         f.write(f"### {title}\n\n")
        #         f.write(formatted_df.to_markdown(index=False))
        #     print(f"[ZAPIS MD] Tabelę Markdown zapisano w: {md_filename}")

        # =========================================================================
        # BEZPIECZNE GENEROWANIE TABELI INLINE HTML (STYL PASTELOWY BABY BLUE)
        # =========================================================================
        if save_md:
            if not save_name_suffix:
                save_name_suffix = f"default_name_table_{file_label}_{category_name.lower()}"
            
            # Nowe style: Wyraźniejsza, ciemniejsza czcionka o wysokim kontraście
            th_style = "style='background-color: #e0f2fe; color: #0369a1; padding: 12px 14px; text-align: left; font-weight: 700; font-family: -apple-system, BlinkMacSystemFont, \"Segoe UI\", Helvetica, Arial, sans-serif; font-size: 13px; border-bottom: 2px solid #bae6fd;'"
            td_base  = "padding: 11px 14px; border-bottom: 1px solid #e2e8f0; color: #1e293b; font-family: -apple-system, BlinkMacSystemFont, \"Segoe UI\", Helvetica, Arial, sans-serif; font-size: 13px;"
            
            # Budujemy strukturę tabeli
            html_rows = []
            html_rows.append("<table style='border-collapse: collapse; width: 100%; border: 1px solid #cbd5e1; border-radius: 6px; overflow: hidden;'>")
            html_rows.append("  <thead>")
            html_rows.append("    <tr>")
            for h in headers:
                html_rows.append(f"      <th {th_style}>{h}</th>")
            html_rows.append("    </tr>")
            html_rows.append("  </thead>")
            html_rows.append("  <tbody>")
            
            # Wiersze danych
            for idx, row in enumerate(rows):
                bg_color = "#f8fafc" if idx % 2 == 0 else "#ffffff"
                
                html_rows.append(f"    <tr style='background-color: {bg_color};'>")
                for col_idx, val in enumerate(row):
                    
                    # Kolumna 1 (Strategia): Wyraźny, głęboki kolor
                    if col_idx == 0:
                        custom_style = f"{td_base} font-weight: 600; color: #0f172a;"
                    
                    # Kolumna 2: Konfiguracja (Mocniejszy, techniczny monospace)
                    elif col_idx == 1:
                        custom_style = f"{td_base} font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 12px; color: #334155; font-weight: 600;"
                    
                    # Kolumna 3: Liczba sygnałów (Stonowany szary, ale czytelny)
                    elif col_idx == 2:
                        custom_style = f"{td_base} color: #64748b; font-weight: 500;"
                        
                    # Kolumna 4: Średnie K (Nadal w miętowym pastelu dla świetnego kontrastu z niebieskim nagłówkiem)
                    elif col_idx == 3:
                        custom_style = f"{td_base} font-weight: 700; color: #0f172a; background-color: #e6f4ea;"
                        
                    # Pozostałe kolumny z metrykami
                    else:
                        custom_style = td_base
                        
                    html_rows.append(f"      <td style='{custom_style}'>{val}</td>")
                html_rows.append("    </tr>")
                
            html_rows.append("  </tbody>")
            html_rows.append("</table>")
            
            complete_html_table = "\n".join(html_rows)
            
            # Zapis do pliku z poprawionymi uniwersalnymi ukośnikami ścieżki
            md_filename = os.path.join(output_dir, f"{save_name_suffix}.md")
            with open(md_filename, "w", encoding="utf-8") as f:
                f.write(f"##### {title}\n\n")
                f.write(complete_html_table)
                
            print(f"[ZAPIS MODERN HTML] Tabelę zapisano w: {md_filename}")

        ReportTableRenderer.render(title, headers, rows)

class EnergyTester:
    def __init__(self, dataset):
        """
        Tester masowy dedykowany dla Kryterium Energetycznego.
        Args:
            dataset (dict): Słownik list sygnałów (aprbs, multisine, noise)
        """
        self.dataset = dataset

    def run(self, category_name, use_custom_fft=True):
        """
        Uruchamia testy energetyczne dla wybranej kategorii i zwraca surową listę wyników.
        Args:
            category_name (str): Nazwa kategorii sygnałów do testowania ('aprbs', 'multisine', 'noise')
            use_custom_fft (bool): Flaga wyboru silnika obliczeniowego (True=Autorski, False=NumPy)
        Returns:    
            list: Surowa lista słowników z wynikami testów dla każdego sygnału i progu energetycznego
        """
        if category_name not in self.dataset:
            print(f"[BŁĄD] Brak kategorii '{category_name}' w zbiorze danych dla EnergyTester.")
            return []

        signals = self.dataset[category_name]
        results = []
        energy_thresholds = [0.99, 0.999, 0.9999]

        desc_text = f"Kryterium Energetyczne: {category_name.upper()}"
        
        # Narzucamy stały format: opis wyrównany do lewej na 75 znaków, po nim dwukropek i pasek
        for idx, signal in enumerate(tqdm(
            signals, 
            bar_format='{desc:<70} {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]',
            desc=desc_text
        )):
            # Obliczamy pełne widmo tylko RAZ dla danego sygnału
            if use_custom_fft:
                _, coeffs = DiscreteFourier.transform(signal.t, signal.y)
            else:
                coeffs = np.fft.fft(signal.y)

            for eth in energy_thresholds:
                energy_res = EnergyAnalyzer.analyze_energy_distribution(coeffs, N=len(signal.y), threshold=eth)
                
                # Bezpieczne wyciąganie progu K (obsługa słownika lub surowej liczby)
                if isinstance(energy_res, dict):
                    k_energy = int(energy_res['k_threshold'])
                else:
                    k_energy = int(energy_res)
                
                # Rekonstrukcja sygnału w czasie
                if use_custom_fft:
                    f_trimmed = DiscreteFourier.trim_spectrum(coeffs, k_energy)
                    y_rec = DiscreteFourier.inverse_transform(f_trimmed)
                else:
                    magnitudes = np.abs(coeffs)
                    threshold_val = np.sort(magnitudes)[-k_energy] if k_energy < len(magnitudes) else 0
                    f_trimmed = np.where(magnitudes >= threshold_val, coeffs, 0)
                    y_rec = np.fft.ifft(f_trimmed, n=len(signal.y)).real
                
                # Ewaluacja metryk jakości
                metrics = SignalMetrics.evaluate_reconstruction(signal.y, y_rec)
                
                results.append({
                    "Strategia": "Energetyczne",
                    "Konfiguracja": f"Prog_Energii_{eth*100}%",
                    "Indeks sygnału": idx,
                    "Wymagane K": k_energy,
                    "MSE": metrics["MSE"],
                    "RMSE": metrics["RMSE"],
                    "Max Error": metrics["MAX ERROR"],
                    "PRD": metrics["Wskaźnik zniekształcenia PRD"]
                })
        return results

class FidelityTester:
    def __init__(self, dataset):
        """
        Tester masowy dedykowany dla Kryterium Dokładnościowego (Fidelity).
        Args:
            dataset (dict): Słownik list sygnałów (aprbs, multisine, noise)
        """
        self.dataset = dataset

    def run(self, category_name, mode='mse', use_custom_fft=True):
        """
        KROK 1: Uruchamia testy dokładnościowe dla wybranej kategorii i zwraca surową listę wyników.
        Args:
            category_name (str): Nazwa kategorii sygnałów do testowania ('aprbs', 'multisine', 'noise')
            mode (str): Metryka błędu do analizy ('mse' lub 'max_error')
            use_custom_fft (bool): Flaga wyboru silnika obliczeniowego (True=Autorski, False=NumPy)
        Returns:        
            list: Surowa lista słowników z wynikami testów dla każdego sygnału i progu dokładności
        """
        if category_name not in self.dataset:
            print(f"[BŁĄD] Brak kategorii '{category_name}' w zbiorze danych dla FidelityTester.")
            return []

        signals = self.dataset[category_name]
        results = []
        fidelity_thresholds = [0.01, 0.1, 1.0]

        desc_text = f"Kryterium Fidelity: {category_name.upper()} - Silnik: {'Autorski' if use_custom_fft else 'NumPy'} - Metryka: {mode.upper()}"

        # Używamy dokładnie takiego samego szablonu bar_format i szerokości 75 znaków
        for idx, signal in enumerate(tqdm(
            signals, 
            bar_format='{desc:<75} {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]',
            desc=desc_text
        )):            # Obliczamy pełne widmo tylko RAZ dla danego sygnału
            if use_custom_fft:
                _, coeffs = DiscreteFourier.transform(signal.t, signal.y)
            else:
                coeffs = np.fft.fft(signal.y)
            
            # --- TESTY DLA MODUŁU self.mode ---
            for fth in fidelity_thresholds:
                analysis = FidelityAnalyzer.analyze_by_error(
                    original_y=signal.y, coeffs=coeffs, threshold=fth, mode=mode, use_numpy=not use_custom_fft
                )
                k_fid = int(analysis['k_threshold'])
                metrics = SignalMetrics.evaluate_reconstruction(signal.y, analysis['reconstructed_y'])
                
                results.append({
                    "Strategia": f"Fidelity ({mode.upper()})",
                    "Konfiguracja": f"Tolerancja_{fth}",
                    "Indeks sygnału": idx,
                    "Wymagane K": k_fid,
                    "MSE": metrics["MSE"],
                    "RMSE": metrics["RMSE"],
                    "Max Error": metrics["MAX ERROR"],
                    "PRD": metrics["Wskaźnik zniekształcenia PRD"]
                })
        return results
