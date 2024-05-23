from openai import OpenAI
from dotenv import load_dotenv
import os
import argparse


def transcribe_directory(input_folder):
    load_dotenv()  # Load environment variables
    client = OpenAI()  # Initialize the OpenAI client

    all_transcriptions = []  # List to hold all transcriptions

    # Loop through each file in the directory
    for filename in os.listdir(input_folder):
        if filename.endswith(".wav"):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, "rb") as audio_file:
                print(f"Transcribing {filename}...")
                try:
                    transcription = client.audio.transcriptions.create(
                        model="whisper-1", file=audio_file, response_format="text"
                    )
                    if isinstance(transcription, str):
                        all_transcriptions.append(transcription)
                    else:
                        # Print the response to see what it is when not a string
                        print(f"Unexpected response format: {transcription}")
                        all_transcriptions.append(
                            "Failed to transcribe due to unexpected response format."
                        )
                except Exception as e:
                    print(f"Failed to transcribe {filename}. Error: {str(e)}")
                    all_transcriptions.append(
                        f"Failed to transcribe {filename}. Error: {str(e)}"
                    )

    # Write all transcriptions to a single text file
    output_file_path = os.path.join(input_folder, "complete_transcription.txt")
    with open(output_file_path, "w") as output_file:
        for transcription in all_transcriptions:
            output_file.write(transcription + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe all WAV files in a directory and output to a text file."
    )
    parser.add_argument(
        "input_folder", type=str, help="Path to the input folder containing WAV files."
    )
    args = parser.parse_args()

    transcribe_directory(args.input_folder)


if __name__ == "__main__":
    main()
