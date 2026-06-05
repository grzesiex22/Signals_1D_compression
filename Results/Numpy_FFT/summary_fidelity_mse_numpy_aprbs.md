### Kryterium Dokładnościowe (Fidelity MSE) - Zbiorczy raport dla sygnałów: APRBS

<style>
                .premium-table-container {
                    margin: 20px 0;
                    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                    border-radius: 8px;
                    overflow: hidden;
                    border: 1px solid #e2e8f0;
                }
                .premium-table {
                    border-collapse: collapse;
                    width: 100%;
                    font-family: 'Inter', 'Segoe UI', Helvetica, Arial, sans-serif;
                    font-size: 13px;
                    background-color: #ffffff;
                }
                .premium-table th {
                    background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
                    color: #ffffff;
                    padding: 14px 16px;
                    text-align: left;
                    font-weight: 600;
                    text-transform: uppercase;
                    font-size: 11px;
                    letter-spacing: 0.05em;
                    border: none;
                }
                .premium-table td {
                    padding: 12px 16px;
                    border-bottom: 1px solid #f1f5f9;
                    color: #334155;
                }
                /* Efekt zebry - naprzemienne wiersze */
                .premium-table tr:nth-child(even) {
                    background-color: #f8fafc;
                }
                /* Efekt podświetlenia wiersza po najechaniu */
                .premium-table tr:hover {
                    background-color: #f1f5f9;
                    transition: background-color 0.2s ease;
                }
                /* Wyróżnienie pierwszej kolumny (Strategia) */
                .premium-table td:nth-child(1) {
                    font-weight: 500;
                    color: #1e293b;
                }
                /* Wyróżnienie drugiej kolumny (Konfiguracja) i nadanie jej koloru akcentu */
                .premium-table td:nth-child(2) {
                    font-weight: 600;
                    color: #2563eb;
                }
                /* Wyróżnienie kolumny ze Średnim K (kolumna 4) */
                .premium-table td:nth-child(4) {
                    font-weight: 700;
                    color: #0f172a;
                    background-color: rgba(37, 99, 235, 0.03);
                }
            </style>
            
<div class="premium-table-container">
<table class="dataframe premium-table">
  <thead>
    <tr style="text-align: right;">
      <th>Strategia</th>
      <th>Konfiguracja</th>
      <th>Liczba sygnałów</th>
      <th>Średnie K</th>
      <th>Min K</th>
      <th>Max K</th>
      <th>Std(K)</th>
      <th>Średnie MSE</th>
      <th>Średnie RMSE</th>
      <th>Średni Max Error</th>
      <th>Średni PRD</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Fidelity (MSE)</td>
      <td>Tolerancja_0.01</td>
      <td>100</td>
      <td>1986.6</td>
      <td>976</td>
      <td>2803</td>
      <td>369.37</td>
      <td>0.00999</td>
      <td>0.1000</td>
      <td>1.50</td>
      <td>1.66%</td>
    </tr>
    <tr>
      <td>Fidelity (MSE)</td>
      <td>Tolerancja_0.1</td>
      <td>100</td>
      <td>290.5</td>
      <td>102</td>
      <td>586</td>
      <td>97.03</td>
      <td>0.09973</td>
      <td>0.3158</td>
      <td>3.51</td>
      <td>5.24%</td>
    </tr>
    <tr>
      <td>Fidelity (MSE)</td>
      <td>Tolerancja_1.0</td>
      <td>100</td>
      <td>29.9</td>
      <td>11</td>
      <td>67</td>
      <td>9.67</td>
      <td>0.97716</td>
      <td>0.9885</td>
      <td>4.23</td>
      <td>16.41%</td>
    </tr>
  </tbody>
</table>
</div>