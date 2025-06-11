import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write, read
from scipy import signal
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Global variables
FREQ = 44100  # Sampling frequency
OUTPUT_DIR = "recordings"

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def record_audio():
    # Get duration from user
    duration = float(input("Enter recording duration in seconds: "))
    
    print(f"\nRecording started for {duration} seconds...")
    recording = sd.rec(int(duration * FREQ), samplerate=FREQ, channels=2)
    sd.wait()
    print("Recording finished!")
    
    return recording, duration

def play_audio(audio_data):
    print("\nPlaying audio... Press Ctrl+C to stop.")
    try:
        # Ensure the audio is in the correct format
        if audio_data.dtype != np.float32:
            audio_data = audio_data.astype(np.float32)
        
        # Normalize audio to prevent clipping
        audio_data = audio_data / np.max(np.abs(audio_data))
        
        sd.play(audio_data, FREQ)
        sd.wait()
    except KeyboardInterrupt:
        sd.stop()
        print("\nPlayback stopped by user")
    except Exception as e:
        print(f"\nPlayback error: {str(e)}")

def apply_noise_cancellation(audio_data):
    print("Applying noise cancellation...")
    
    # Convert stereo to mono if necessary
    if len(audio_data.shape) > 1:
        audio_data = np.mean(audio_data, axis=1)
    
    # Apply simple noise reduction using bandpass filter
    nyquist = FREQ / 2
    low_cutoff = 100 / nyquist
    high_cutoff = 3000 / nyquist
    b, a = signal.butter(4, [low_cutoff, high_cutoff], btype='band')
    filtered_audio = signal.filtfilt(b, a, audio_data)
    
    return filtered_audio

def visualize_audio(audio_data, duration, filename=None):
    print("Generating enhanced audio visualization...")
    
    # Convert to mono if stereo
    if len(audio_data.shape) > 1:
        audio_data = np.mean(audio_data, axis=1)
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), height_ratios=[1, 1.5])
    fig.suptitle('Audio Analysis', fontsize=16, y=0.95)
    
    # Plot waveform
    time_array = np.linspace(0, duration, len(audio_data))
    ax1.plot(time_array, audio_data, color='blue', alpha=0.7)
    ax1.set_xlabel('Time (seconds)')
    ax1.set_ylabel('Amplitude')
    ax1.grid(True, alpha=0.3)
    
    # Plot spectrogram
    spec, freqs, times, im = ax2.specgram(audio_data, 
                                         NFFT=1024, 
                                         Fs=FREQ, 
                                         noverlap=512, 
                                         cmap='viridis',
                                         scale='dB',
                                         mode='magnitude')
    
    ax2.set_title('Spectrogram')
    ax2.set_xlabel('Time (seconds)')
    ax2.set_ylabel('Frequency (Hz)')
    
    # Add colorbar
    cbar = fig.colorbar(im, ax=ax2)
    cbar.set_label('Intensity (dB)', rotation=270, labelpad=15)
    
    # Adjust frequency axis to show in kHz
    ax2.set_ylim(0, FREQ/2)
    y_ticks = np.linspace(0, FREQ/2, 10)
    ax2.set_yticks(y_ticks)
    ax2.set_yticklabels([f'{int(y/1000)}k' for y in y_ticks])
    
    # Add grid to spectrogram
    ax2.grid(True, alpha=0.3, linestyle='--')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save or show based on whether filename is provided
    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def main():
    try:
        # Record audio
        recording, duration = record_audio()
        
        # Generate timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save original audio
        original_path = os.path.join(OUTPUT_DIR, f"original_{timestamp}.wav")
        write(original_path, FREQ, recording)
        print(f"\nOriginal audio saved: {original_path}")
        
        # Apply noise cancellation
        filtered_audio = apply_noise_cancellation(recording)
        filtered_path = os.path.join(OUTPUT_DIR, f"filtered_{timestamp}.wav")
        write(filtered_path, FREQ, filtered_audio)
        print(f"Filtered audio saved: {filtered_path}")
        
        # Create and save initial visualization
        viz_path = os.path.join(OUTPUT_DIR, f"visualization_{timestamp}.png")
        visualize_audio(recording, duration, viz_path)
        print(f"Enhanced visualization saved: {viz_path}")
        
        # Playback options
        while True:
            print("\nOptions:")
            print("1. Play original recording")
            print("2. Play filtered audio")
            print("3. Show visualization")
            print("4. Exit")
            
            choice = input("Enter your choice (1-4): ")
            
            if choice == '1':
                play_audio(recording)
            elif choice == '2':
                play_audio(filtered_audio)
            elif choice == '3':
                print("\nDisplaying visualization... Close the plot window to continue.")
                # Show interactive visualization
                visualize_audio(recording, duration)
            elif choice == '4':
                print("\nExiting program...")
                break
            else:
                print("Invalid choice. Please try again.")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main()