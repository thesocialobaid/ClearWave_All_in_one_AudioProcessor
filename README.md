# ClearWave_All_in_one_AudioProcessor

##Overview: 
ClearWave is a powerful and user-friendly audio processing application that integrates recording, playback, noise cancellation, waveform visualization, and speech-to-text transcription into a single platform. Designed for both experimentation and practical use, it enables users to manipulate and interpret audio in real-time — ideal for educational tools, research, or accessibility applications.


## 🧰 Tech Stack: 
Python – Core language for implementation and backend logic

NumPy & Matplotlib – Used for signal processing and waveform visualization

pyaudio / sounddevice – For real-time audio input/output

speech_recognition / Whisper – Converts recorded audio to readable text

scipy / noisereduce – Applied basic and advanced noise reduction algorithms

## 🧩 System Architecture 
1. Audio Input → 2. Noise Reduction → 3. Waveform Visualization → 4. Playback → 5. Transcription

Audio Input & Playback: Users can record and replay audio through their microphone using low-latency, real-time processing libraries.

Noise Reduction: Integrated filtering algorithms remove background disturbances to enhance audio clarity before transcription.

Visualization: The tool plots real-time waveforms using matplotlib, offering insight into audio amplitude and duration.

Speech-to-Text Transcription: Leveraging a speech recognition engine, it converts clean audio into readable text output for accessibility or documentation.

