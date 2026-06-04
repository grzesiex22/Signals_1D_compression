import pandas as pd
from IPython.display import display

class ReportTableRenderer:
    @staticmethod
    def render(title, headers, rows):
        """
        Generuje i wyświetla elegancką, nowoczesną tabelę HTML w Jupyter Notebooku.
        
        Args:
            title (str): Tytuł wyświetlany bezpośrednio nad tabelą jako podpis.
            headers (list): Lista zawierająca nazwy nagłówków kolumn.
            rows (list of lists): Lista wierszy, gdzie każdy wiersz to lista wartości.
        """
        # 1. Konwersja danych do formatu słownika dla Pandas
        data_dict = {headers[i]: [row[i] for row in rows] for i in range(len(headers))}
        
        # 2. Tworzenie obiektu DataFrame
        df = pd.DataFrame(data_dict)
        
        # 3. Definicja i aplikacja nowoczesnego stylu CSS wraz z tytułem (caption)
        styled_df = df.style.set_caption(title).set_table_styles([
            # Styl dla tytułu nad tabelą (pogrubiony, wyśrodkowany, z odstępem)
            {'selector': 'caption', 'props': [
                ('caption-side', 'top'),
                ('font-family', 'Segoe UI, sans-serif'),
                ('font-size', '15px'),
                ('font-weight', 'bold'),
                ('color', "#95b3e5"),
                ('text-align', 'center'),
                ('padding-bottom', '10px')
            ]},
            # Styl nagłówka (ciemny grafit, elegancki font)
            {'selector': 'th', 'props': [
                ('background-color', '#2d3748'), 
                ('color', 'white'), 
                ('font-family', 'Segoe UI, sans-serif'),
                ('padding', '12px 16px'),
                ('font-weight', '600'),
                ('text-align', 'center')
            ]},
            # Styl komórek z danymi
            {'selector': 'td', 'props': [
                ('padding', '10px 16px'),
                ('font-family', 'Segoe UI, sans-serif'),
                ('border-bottom', '1px solid #e2e8f0'),
                ('background-color', '#f8fafc')
            ]},
            # Wyrównanie: tekst do lewej, liczby do prawej
            {'selector': 'td.col0', 'props': [('text-align', 'left'), ('color', '#1a202c')]},
            {'selector': 'td.col1', 'props': [('text-align', 'right'), ('color', '#1d4ed8'), ('font-weight', 'bold')]}
        ]).hide(axis='index')  # Ukrywamy indeksy wierszy
        
        # 4. Wyświetlenie ostylowanej tabeli
        display(styled_df)