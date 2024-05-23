import wave
import os


def split_wav(file_path, output_folder="output_chunks", chunk_size_mb=22):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Calculate chunk size in bytes, consider overhead for headers and metadata
    chunk_size_bytes = (
        chunk_size_mb * 1024 * 1024
    ) - 100  # Reduce slightly to account for headers

    # Open the WAV file
    with wave.open(file_path, "rb") as wav:
        n_channels = wav.getnchannels()
        samp_width = wav.getsampwidth()
        frame_rate = wav.getframerate()
        n_frames = wav.getnframes()
        total_bytes_read = 0
        part = 1

        while (
            total_bytes_read
            < wav.getnframes() * wav.getsampwidth() * wav.getnchannels()
        ):
            # Calculate the number of frames that fit into the remaining chunk size
            remaining_bytes = (
                wav.getnframes() * wav.getsampwidth() * wav.getnchannels()
                - total_bytes_read
            )
            max_frame_bytes = chunk_size_bytes - 44  # Subtract the size of headers
            frames_to_read = min(max_frame_bytes, remaining_bytes) // (
                n_channels * samp_width
            )

            # Read frames
            data = wav.readframes(frames_to_read)

            # Write the chunk to a new file in the specified folder
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

            # Update total bytes read and part number
            total_bytes_read += len(data)
            part += 1


# Example usage
split_wav(
    "./audio_files/second_interview.wav",
    output_folder="./splitted_audios/second_interview",
)
