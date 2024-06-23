import os
import re


def create_files_from_markdown(file_path, output_directory):
    # Read the markdown content from the file
    with open(file_path, "r", encoding="utf-8") as file:
        markdown_content = file.read()

    # Split the markdown content by lines
    lines = markdown_content.split("\n")

    current_h1 = None
    current_h2 = None
    current_content = []

    for line in lines:
        if line.startswith("# "):
            # New H1 header
            if current_h1 and current_h2:
                # Write the last section to a file
                write_section_to_file(
                    output_directory, current_h1, current_h2, current_content
                )
            current_h1 = line[2:].strip()
            current_h2 = None
            current_content = []
        elif line.startswith("# "):
            # New H2 header
            if current_h2:
                # Write the last section to a file
                write_section_to_file(
                    output_directory, current_h1, current_h2, current_content
                )
            current_h2 = line[3:].strip()
            current_content = []
        else:
            current_content.append(line)

    # Write the last section to a file
    if current_h1 and current_h2:
        write_section_to_file(output_directory, current_h1, current_h2, current_content)


def write_section_to_file(output_directory, h1, h2, content):
    # Create directory for H1 if it doesn't exist
    h1_directory = os.path.join(output_directory, sanitize_filename(h1))
    os.makedirs(h1_directory, exist_ok=True)

    # Create file for H2
    file_path = os.path.join(h1_directory, sanitize_filename(h2) + ".md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# " + h2 + "\n")
        f.write("\n".join(content))


def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "_", filename)


# Example usage
file_path = "./Palladium Fantasy.md"  # Replace with the path to your Markdown file
output_directory = "./output_markdown"
create_files_from_markdown(file_path, output_directory)
