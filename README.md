# Audio Transcription Tool

This repository provides tools and scripts for converting and transcribing audio files. It uses a local version of the Whisper model to process WAV files, converting them to a suitable format, splitting them into manageable chunks, and transcribing the audio content into text. The tools are designed to handle large or lengthy audio files efficiently.

## Setup Instructions

### 1. Clone whisper

Clone the whisper repository from GitHub:

```bash
git clone https://github.com/ggerganov/whisper.cpp.git
```

Follow installation instructions from: https://github.com/ggerganov/whisper.cpp?tab=readme-ov-file#quick-start

### 2. Clone This Repository

Clone the audio transcriber repository:

```bash
git clone https://github.com/marvinknoll/audio_transcriber.git
```

### 3. Navigate to the Repository Directory

Change into the `audio_transcriber` directory:

```bash
cd audio_transcriber
```

### 4. Install Dependencies

Install the necessary dependencies using `pdm`:

```bash
pdm install
```

### 5. Install FFmpeg

FFmpeg is required for audio file conversion. Install FFmpeg using the following command:

```bash
sudo apt-get install ffmpeg

```

## Converting and Transcribing Audio Files

### Prepare Your Audio File

Ensure your audio file is in WAV format. If not, convert it using your preferred tool (numerous online converters are available).

### Run the Transcription Script

To convert and transcribe an audio file, use the following command:

```bash
pdm run python local_split_convert_and_transcribe.py "./path/to/audio/file.wav" -l <audio_language_code>
```

Replace `<audio_language_code>` with the appropriate language code for the audio recording. To see the available languages, visit:

[Whisper Language Codes](https://github.com/ggerganov/whisper.cpp.git)

### What the Script Does

The script performs the following actions:

1. **Converts the audio file to 16 kHz using FFmpeg.**
2. **Splits the converted WAV into smaller chunks (up to 23,1 MB each) to optimize processing.**
3. **Transcribes each chunk using the Whisper model.**
4. **Compiles all transcriptions into a single text file located in `/splitted_audios/filename/complete_transcription.txt`.**
