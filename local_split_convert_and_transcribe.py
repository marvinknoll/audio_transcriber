# For this to work, clone https://github.com/ggerganov/whisper.cpp.git to ../whisper.cpp/
# Convert the audio file to .wav format and put it into the folder ./original_wav_files/
# This script converts the .wav to 16 kHz using ffmpeg, then splits it into smaller chunk_size_mb
# for whisper(max 50mb), transcribes every chunk and creates the complete_transcription.txt
# Example usage: pdm run python local_split_convert_and_transcribe.py "./original_wav_files/interview_1.wav" -l de
import os
import argparse
import subprocess
import wave


def convert_sample_rate_ffmpeg(input_path, output_path, sample_rate=16000):
    command = ["ffmpeg", "-i", input_path, "-ar", str(sample_rate), output_path]
    subprocess.run(command, capture_output=True)


def split_wav(file_path, output_folder, chunk_size_mb=22):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    chunk_size_bytes = (chunk_size_mb * 1024 * 1024) - 100

    with wave.open(file_path, "rb") as wav:
        n_channels = wav.getnchannels()
        samp_width = wav.getsampwidth()
        frame_rate = wav.getframerate()
        total_bytes_read = 0
        part = 1

        while (
            total_bytes_read
            < wav.getnframes() * wav.getsampwidth() * wav.getnchannels()
        ):
            remaining_bytes = (
                wav.getnframes() * wav.getsampwidth() * wav.getnchannels()
                - total_bytes_read
            )
            max_frame_bytes = chunk_size_bytes - 44
            frames_to_read = min(max_frame_bytes, remaining_bytes) // (
                n_channels * samp_width
            )
            data = wav.readframes(frames_to_read)
            chunk_filename = os.path.join(output_folder, f"chunk_{part}.wav")
            with wave.open(chunk_filename, "wb") as chunk_wav:
                chunk_wav.setparams(
                    (
                        n_channels,
                        samp_width,
                        frame_rate,
                        frames_to_read,
                        "NONE",
                        "not compressed",
                    )
                )
                chunk_wav.writeframes(data)
            total_bytes_read += len(data)
            part += 1


def transcribe_directory(input_folder, language_code):
    files = [f for f in os.listdir(input_folder) if f.endswith(".wav")]
    files.sort()

    all_transcriptions = []

    for filename in files:
        file_path = os.path.join(input_folder, filename)
        print(f"Transcribing {filename} using language code '{language_code}'...")
        try:
            command = [
                "../whisper.cpp/main",
                "-m",
                "../whisper.cpp/models/ggml-large-v3.bin",
                "-l",
                language_code,
                "-f",
                file_path,
                "-otxt",
                "-nt",
            ]
            print(command)
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                all_transcriptions.append((filename, result.stdout))
            else:
                print(f"Error transcribing {filename}: {result.stderr}")
                all_transcriptions.append(
                    (
                        filename,
                        f"Failed to transcribe {filename}. Error: {result.stderr}",
                    )
                )
        except Exception as e:
            print(
                f"Failed to execute transcription command for {filename}. Error: {str(e)}"
            )
            all_transcriptions.append(
                (
                    filename,
                    f"Failed to execute transcription command for {filename}. Error: {str(e)}",
                )
            )

    all_transcriptions.sort(key=lambda x: x[0])

    output_file_path = os.path.join(input_folder, "complete_transcription.txt")
    try:
        with open(output_file_path, "w") as output_file:
            for _, transcription in all_transcriptions:
                output_file.write(transcription + "\n\n")
    except Exception as e:
        print(f"Failed to write transcriptions to file. Error: {str(e)}")


def process_file(file_path, language_code):
    base_filename = os.path.basename(file_path)
    converted_path = file_path.replace(".wav", "_converted.wav")
    split_folder = f"./splitted_audios/{base_filename.replace('.wav', '')}/"

    # Convert sample rate
    convert_sample_rate_ffmpeg(file_path, converted_path)

    # Split the WAV file
    split_wav(converted_path, split_folder)

    # Transcribe the split WAV files
    transcribe_directory(split_folder, language_code)

    # Optionally, clean up the converted file if no longer needed
    os.remove(converted_path)


def main():
    parser = argparse.ArgumentParser(
        description="Process a WAV file by converting, splitting, and transcribing."
    )
    parser.add_argument("file_path", type=str, help="Path to the WAV file.")
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        default="en",
        help="Language code for transcription.",
    )
    args = parser.parse_args()

    process_file(args.file_path, args.language)


if __name__ == "__main__":
    main()
