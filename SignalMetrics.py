import numpy as np

class SignalMetrics:
    @staticmethod
    def calculate_energy(y):
        """Oblicza całkowitą energię sygnału w dziedzinie czasu."""
        # np.real() odrzuca mikro-część urojoną powstałą z IDFT
        y = np.real(np.asarray(y))
        return float(np.sum(y ** 2))

    @staticmethod
    def mse(y_true, y_pred):
        """Błąd średniokwadratowy (Mean Squared Error)."""
        y_true = np.real(np.asarray(y_true))
        y_pred = np.real(np.asarray(y_pred))
        return float(np.mean((y_true - y_pred) ** 2))

    @staticmethod
    def rmse(y_true, y_pred):
        """Pierwiastek błędu średniokwadratowego (Root Mean Squared Error)."""
        return float(np.sqrt(SignalMetrics.mse(y_true, y_pred)))

    @staticmethod
    def max_error(y_true, y_pred):
        """Maksymalny błąd bezwzględny (Max Absolute Error)."""
        y_true = np.real(np.asarray(y_true))
        y_pred = np.real(np.asarray(y_pred))
        return float(np.max(np.abs(y_true - y_pred)))

    @staticmethod
    def prd(y_true, y_pred):
        """
        Percent Root-mean-square Difference (PRD).
        Standardowy wskaźnik zniekształcenia sygnału po kompresji (w procentach).
        """
        y_true = np.real(np.asarray(y_true))
        y_pred = np.real(np.asarray(y_pred))
        
        numerator = np.sum((y_true - y_pred) ** 2)
        denominator = np.sum(y_true ** 2)
        
        if denominator == 0:
            return 0.0
            
        return float(np.sqrt(numerator / denominator) * 100)

    @staticmethod
    def evaluate_reconstruction(y_true, y_pred):
        """
        Generuje gotowy zestaw metryk dla rekonstrukcji sygnału 1D.
        Zwraca czysty słownik.
        """
        energy_orig = SignalMetrics.calculate_energy(y_true)
        energy_rec = SignalMetrics.calculate_energy(y_pred)
        energy_loss_pct = (1.0 - (energy_rec / energy_orig)) * 100 if energy_orig != 0 else 0.0

        return {
            "Energia oryginału (w dziedzinie czasu)": energy_orig,
            "Energia po rekonstrukcji (w dziedzinie czasu)": energy_rec,
            "Procentowa strata energii": energy_loss_pct,
            "MSE": SignalMetrics.mse(y_true, y_pred),
            "RMSE": SignalMetrics.rmse(y_true, y_pred),
            "MAX ERROR": SignalMetrics.max_error(y_true, y_pred),
            "Wskaźnik zniekształcenia PRD": SignalMetrics.prd(y_true, y_pred)
        }