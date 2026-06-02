import numpy as np
import scipy.io.wavfile as wav
import datetime
from Fourier import DiscreteFourier
import os

rate, data = wav.read('data/source/gitara_strun_ma_wiele.wav')

# Jeśli audio jest stereo, uśredniamy je do mono 
if len(data.shape) > 1:
    data = data.mean(axis=1)

data = data.astype(float)

coeffs = np.fft.rfft(data)

#fourier_engine = DiscreteFourier(rate, data)
#coeffs = fourier_engine.transform()

# chcemy zachować tylko 1% najsilniejszych składowych
compression_ratio = 0.1
amplitudes = np.abs(coeffs)
threshold = np.percentile(amplitudes, (1 - compression_ratio) * 100)

coeffs_compressed = coeffs.copy()
coeffs_compressed[amplitudes < threshold] = 0

compressed_data = np.fft.irfft(coeffs_compressed)

compressed_data = np.int16(compressed_data)

date = datetime.datetime.now()
file_name = f"wynik-{date.strftime('%d_%m_%Y_%H_%M')}"

# Dodaj to przed linijką wav.write
output_dir = 'data/compressed'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Utworzono folder: {output_dir}")

wav.write(f'{output_dir}/{file_name}.wav', rate, compressed_data)
