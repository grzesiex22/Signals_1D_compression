### Kryterium Dokładnościowe (Fidelity Max Error) - Zbiorczy raport dla sygnałów: APRBS

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
      <td>Fidelity (MAX_ERROR)</td>
      <td>Tolerancja_0.01</td>
      <td>100</td>
      <td>4897.2</td>
      <td>4839</td>
      <td>4927</td>
      <td>17.48</td>
      <td>0.00000708</td>
      <td>0.00265</td>
      <td>0.00984</td>
      <td>0.0440%</td>
    </tr>
    <tr>
      <td>Fidelity (MAX_ERROR)</td>
      <td>Tolerancja_0.1</td>
      <td>100</td>
      <td>4239.1</td>
      <td>4005</td>
      <td>4423</td>
      <td>83.53</td>
      <td>0.00045075</td>
      <td>0.02109</td>
      <td>0.09953</td>
      <td>0.3497%</td>
    </tr>
    <tr>
      <td>Fidelity (MAX_ERROR)</td>
      <td>Tolerancja_1.0</td>
      <td>100</td>
      <td>2487.4</td>
      <td>1980</td>
      <td>2753</td>
      <td>146.20</td>
      <td>0.00649071</td>
      <td>0.07979</td>
      <td>0.99913</td>
      <td>1.3221%</td>
    </tr>
  </tbody>
</table>
</div>