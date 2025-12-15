import cv2
import numpy as np
import os
import random
from moviepy.editor import VideoFileClip, AudioFileClip, ImageSequenceClip
from scipy.io.wavfile import write

# ==========================================
# 🧬 METAMORPHOSIS ENGINE v1.0
# Theme: IV - DEEP ABYSS (Biyo-Dijital Dönüşüm)
# Author: imagine-fastq
# ==========================================

def generate_abyss_audio(duration, fps=30):
    """
    Kafkaesk 'Derin Uçurum' ses sentezi.
    40Hz-60Hz arası düşük frekanslı drone sesi ve rastgele 'Sonar' sinyalleri üretir.
    """
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # 1. Katman: The Void (Düşük Frekanslı Drone - 40Hz)
    # Okyanus tabanı hissi veren sinüs dalgası
    drone_base = 0.5 * np.sin(2 * np.pi * 40 * t)
    
    # 2. Katman: Modülasyon (LFO - Low Frequency Oscillation)
    # Sesi dalgalandırır (Nefes alıp verme gibi)
    lfo = 0.5 * (1 + np.sin(2 * np.pi * 0.2 * t))
    drone_modulated = drone_base * lfo

    # 3. Katman: Sonar Pingleri (Veri Sinyalleri)
    # Rastgele anlarda yüksek frekanslı "bip" sesleri
    sonar_layer = np.zeros_like(t)
    num_pings = int(duration / 2) # Her 2 saniyede bir ping ortalaması
    
    for _ in range(num_pings):
        ping_time = random.uniform(0, duration)
        idx = int(ping_time * sample_rate)
        if idx < len(t):
            # Kısa bir yüksek frekans sinyali (800Hz)
            ping_duration = 0.1
            ping_t = np.linspace(0, ping_duration, int(sample_rate * ping_duration))
            ping_wave = 0.3 * np.sin(2 * np.pi * 800 * ping_t) * np.exp(-5 * ping_t) # Sönümlenen ses
            
            end_idx = min(idx + len(ping_wave), len(t))
            sonar_layer[idx:end_idx] += ping_wave[:end_idx-idx]

    # Karıştırma (Mix)
    audio_signal = drone_modulated + sonar_layer
    
    # Normalizasyon (Ses patlamasını önle)
    audio_signal = audio_signal / np.max(np.abs(audio_signal))
    return audio_signal, sample_rate

def apply_genomic_glitch(frame, frame_count):
    """
    Görüntü karesine biyolojik/dijital mutasyon uygular.
    """
    h, w, c = frame.shape
    
    # EFEKT 1: Kırmızı Kod (Red Shift)
    # Görüntünün kırmızı kanalını kaydırarak "ayrışma" yaratır
    shift_amount = int(5 + 10 * np.sin(frame_count * 0.1))
    b, g, r = cv2.split(frame)
    r = np.roll(r, shift_amount, axis=1) # Kırmızı kanalı yana kaydır
    mutated = cv2.merge([b, g, r])

    # EFEKT 2: The Void (Eşikleme)
    # Belirli aralıklarla görüntüyü sadece Siyah-Beyaz iskelete indirger
    if frame_count % 60 < 15: # Her saniyenin ilk 15 karesi
        gray = cv2.cvtColor(mutated, cv2.COLOR_BGR2GRAY)
        _, thresholded = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        # Siyah beyazı 3 kanala çevirip kırmızıyla karıştır
        thresholded_bgr = cv2.cvtColor(thresholded, cv2.COLOR_GRAY2BGR)
        mutated = cv2.addWeighted(mutated, 0.7, thresholded_bgr, 0.3, 0)

    # EFEKT 3: Dijital Yağmur (Binary Rain Noise)
    # Rastgele pikselleri bozar
    noise_density = 0.02 # %2 oranında gürültü
    num_pixels = int(h * w * noise_density)
    for _ in range(num_pixels):
        y_coord = random.randint(0, h - 1)
        x_coord = random.randint(0, w - 1)
        mutated[y_coord, x_coord] = [0, 0, 255] # Saf Kırmızı Noktalar

    return mutated

def main():
    print("\n🧬 METAMORPHOSIS BAŞLATILIYOR...")
    print(">> Hedef: Biyo-Dijital Veri Dönüşümü")
    print(">> Tema: Deep Abyss (Theme 4)\n")

    input_video_path = "input.MOV"
    output_video_path = "imagine_fastq_THEME_4_ABYSS.mp4"
    temp_audio_path = "temp_abyss_audio.wav"

    # 1. Dosya Kontrolü
    if not os.path.exists(input_video_path):
        print(f"⚠️ HATA: '{input_video_path}' bulunamadı!")
        print(">> Lütfen işlenecek videoyu 'input.MOV' adıyla bu klasöre atın.")
        return

    # 2. Video Analizi
    cap = cv2.VideoCapture(input_video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    print(f"📼 Video Analiz Edildi: {duration:.2f} saniye, {width}x{height}, {fps} FPS")

    # 3. Görsel İşleme Döngüsü
    processed_frames = []
    print("🔬 Görsel Mutasyon Başlıyor...")
    
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Mutasyon fonksiyonunu çağır
        glitch_frame = apply_genomic_glitch(frame, frame_count)
        
        # OpenCV BGR formatından RGB formatına çevir (MoviePy için)
        frame_rgb = cv2.cvtColor(glitch_frame, cv2.COLOR_BGR2RGB)
        processed_frames.append(frame_rgb)
        
        frame_count += 1
        if frame_count % 30 == 0:
            print(f"   >> İşleniyor: Kare {frame_count}/{total_frames}")

    cap.release()

    # 4. İşitsel Sentez (Procedural Audio)
    print("🔊 İşitsel Sentez Başlıyor (Deep Abyss)...")
    audio_data, sample_rate = generate_abyss_audio(duration)
    
    # Sesi geçici olarak kaydet
    write(temp_audio_path, sample_rate, (audio_data * 32767).astype(np.int16))

    # 5. Birleştirme (Muxing)
    print("🎬 Render Alınıyor...")
    clip = ImageSequenceClip(processed_frames, fps=fps)
    audio = AudioFileClip(temp_audio_path)
    
    final_clip = clip.set_audio(audio)
    final_clip.write_videofile(output_video_path, codec='libx264', audio_codec='aac')

    # 6. Temizlik
    if os.path.exists(temp_audio_path):
        os.remove(temp_audio_path)

    print(