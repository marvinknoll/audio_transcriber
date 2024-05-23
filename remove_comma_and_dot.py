import re
import os
import argparse


def process_text_file(file_path):
    try:
        # Read the original content from the file
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Remove commas
        content = re.sub(r",", "", content)

        # Replace periods with a space and handle subsequent capitalization
        content = re.sub(
            r"\.\s*(\w)", lambda match: " " + match.group(1).lower(), content
        )

        # Create new filename with "_converted" suffix
        dir_name, base_name = os.path.split(file_path)
        name_part, ext_part = os.path.splitext(base_name)
        new_filename = os.path.join(dir_name, f"{name_part}_converted{ext_part}")

        # Write the modified content to a new file
        with open(new_filename, "w", encoding="utf-8") as file:
            file.write(content)

    except FileNotFoundError:
        print("The file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(
        description="Process a text file to remove commas and adjust periods with lowercased following text."
    )
    parser.add_argument(
        "file_path", type=str, help="Path to the text file to be processed."
    )

    # Parse arguments
    args = parser.parse_args()

    # Process the file
    process_text_file(args.file_path)


if __name__ == "__main__":
    main()
