import struct
import scipy.io.wavfile as wav
import numpy as np

# --- 1. KODER (WAV -> KMP) ---
def koder_wav_do_kmp(wav_path, kmp_path, ratio):
    # Wczytanie surowego WAV
    rate, data = wav.read(wav_path)
    
    # Jeśli stereo, miksujemy do mono
    if len(data.shape) > 1:
        data = data.mean(axis=1)
        
    # KLUCZOWE: Konwersja int16 -> float32 w zakresie [-1.0, 1.0]
    # Bez tego normalizowania FFT dostaje bzika i generuje szum
    data_float = data.astype(np.float32) / 32768.0
    
    # Wykonanie FFT - NUMPY FFT
    coeffs = np.fft.rfft(data_float)

    # # Wykonanie FFT - WŁASNA IMPLEMENTACJA
    # fourier_engine = DiscreteFourier(rate, data)
    # coeffs = fourier_engine.transform()

    # Amplitudy współczynników (moduł) - potrzebne do wyznaczenia progu odcięcia
    amplitudes = np.abs(coeffs)
    
    # Wyznaczenie progu odcięcia (bierzemy X% największych amplitud)
    threshold = np.percentile(amplitudes, (1 - ratio) * 100)
    
    # Znalezienie indeksów współczynników, które przetrwały kompresję
    indices = np.where(amplitudes >= threshold)[0].astype(np.int32)
    
    # Wyciągnięcie tylko tych ważnych współczynników (część rzeczywista i urojona osobnym float32)
    filtered_real = np.real(coeffs[indices]).astype(np.float32)
    filtered_imag = np.imag(coeffs[indices]).astype(np.float32)
    
    # Zapis do czystego pliku binarnego .kmp
    with open(kmp_path, 'wb') as f:
        # Nagłówek: 1. Długość sygnału (int), 2. Liczba indeksów (int), 3. Próbkowanie (int)
        f.write(struct.pack('iii', len(data_float), len(indices), rate))
        # Dane właściwe
        f.write(indices.tobytes())
        f.write(filtered_real.tobytes())
        f.write(filtered_imag.tobytes())
        
    print(f"[KODER] Sukces! Skompresowano {wav_path} -> {kmp_path}")


# --- 2. DEKODER (KMP -> WAV) ---
def dekoder_kmp_do_wav(kmp_path, output_wav_path):
    with open(kmp_path, 'rb') as f:
        # Odczyt nagłówka (3 x int = 12 bajtów)
        total_len, num_indices, rate = struct.unpack('iii', f.read(12))
        
        # Odczyt tablic binarnych
        indices = np.frombuffer(f.read(num_indices * 4), dtype=np.int32)
        filtered_real = np.frombuffer(f.read(num_indices * 4), dtype=np.float32)
        filtered_imag = np.frombuffer(f.read(num_indices * 4), dtype=np.float32)
        
    # Tworzenie pustego widma dla rfft: rozmiar to zawsze (N // 2) + 1
    num_coeffs = (total_len // 2) + 1
    coeffs_rec = np.zeros(num_coeffs, dtype=complex)
    
    # Odtworzenie liczb zespolonych na zakodowanych pozycjach
    coeffs_rec[indices] = filtered_real + 1j * filtered_imag
    
    # Odwrotna transformata (powrót do dźwięku w czasie)
    data_rec_float = np.fft.irfft(coeffs_rec, n=total_len)
    
    # fourier_engine = DiscreteFourier(rate, data)
    # coeffs = fourier_engine.transform()
    
    # Zabezpieczenie przed przesterowaniem (clipping)
    data_rec_float = np.clip(data_rec_float, -1.0, 1.0)
    
    # Powrót do formatu int16 dla klasycznego pliku WAV
    final_wav_data = (data_rec_float * 32767.0).astype(np.int16)
    
    # Zapis finalnego pliku na dysk
    wav.write(output_wav_path, rate, final_wav_data)
    print(f"[DEKODER] Sukces! Zrekonstruowano {kmp_path} -> {output_wav_path}")
    return final_wav_data, rate