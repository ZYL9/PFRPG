import os
import shutil
import re
import markdown2
from ebooklib import epub


def remove_yaml_front_matter(content):
    # Regular expression to match YAML front matter
    yaml_front_matter_pattern = re.compile(
        r"^---\s*\n(.*?\n)^---\s*\n", re.DOTALL | re.MULTILINE
    )
    # Remove the front matter
    cleaned_content = yaml_front_matter_pattern.sub("", content)
    return cleaned_content


def adjust_heading_levels(content, level_offset):
    lines = content.split("\n")
    adjusted_lines = []
    for line in lines:
        if line.startswith("#"):
            # Count the number of leading '#' characters
            heading_level = 0
            while heading_level < len(line) and line[heading_level] == "#":
                heading_level += 1
            # Adjust the heading level
            new_level = heading_level + level_offset
            if new_level > 6:
                # Convert to bold text if heading level exceeds 6
                bold_text = line[heading_level:].strip()
                adjusted_lines.append(f"**{bold_text}**")
            else:
                adjusted_heading = "#" * new_level + line[heading_level:]
                adjusted_lines.append(adjusted_heading)
        else:
            adjusted_lines.append(line)
    return "\n".join(adjusted_lines)


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    """
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    """
    return [atoi(c) for c in re.split(r"(\d+)", text)]


def combine_markdown_files(root_dir):
    combined_content = []

    for current_path, dirs, files in os.walk(root_dir):
        normalized_path = os.path.normpath(current_path)
        if ".vitepress" not in normalized_path.split(
            os.sep
        ) and "public" not in normalized_path.split(os.sep):
            # Sort files to ensure index.md is processed first if present

            files = sorted(files, key=natural_keys)

            level_offset = current_path[len(root_dir) :].count(os.sep)

            # Process index.md first if it exists in the directory
            if "index.md" in files:
                index_path = os.path.join(current_path, "index.md")
                with open(index_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    content = remove_yaml_front_matter(content)
                    if len(content) > 0:
                        adjusted_content = adjust_heading_levels(
                            content, level_offset - 1
                        )
                        combined_content.append(adjusted_content)
                        combined_content.append(
                            '<div STYLE="page-break-after: always;"></div>'
                        )

            # Process other markdown files
            for file in files:
                if file != "index.md" and file.endswith(".md"):
                    file_path = os.path.join(current_path, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        content = remove_yaml_front_matter(content)
                        adjusted_content = adjust_heading_levels(content, level_offset)
                        combined_content.append(adjusted_content)
                        combined_content.append(
                            '<div STYLE="page-break-after: always;"></div>'
                        )

    return "\n".join(combined_content)


def copy_assets_epub(src_dir, epub_book):
    asset_id = 1
    for current_path, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".webp"):
                image_content = open(os.path.join(current_path, file), "rb").read()
                img = epub.EpubImage(
                    uid=f"image_{asset_id}",
                    file_name="./assets/" + file,
                    content=image_content,
                )
                asset_id = asset_id + 1
                epub_book.add_item(img)
    print(f"Total {asset_id} image added")


def split_markdown_by_headings(source_file, dest_dir="./temp"):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    current_title = None
    current_content = []

    with open(source_file, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line.startswith("# "):

                if current_title is not None and current_content:
                    save_content(current_title, current_content, dest_dir)

                current_title = line[2:].strip()
                current_content = []
                current_content.append(line)

            else:
                current_content.append(line)

    if current_title is not None and current_content:
        save_content(current_title, current_content, dest_dir)


def save_content(title, content, dest_dir):
    file_path = os.path.join(dest_dir, f"{title}.md")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(content) + "\n")
    print(f"Saved '{title}.md'")


def md2epub(docs_root, output_epub):
    epub_book = epub.EpubBook()
    epub_book.set_title("Palladium_Fantasy_zh_Hans")
    epub_book.set_language("zh-Hans")
    epub_book.add_author("Author Name")
    epub_book.set_cover("cover.webp", open("./docs/public/cover.webp", "rb").read())

    spine = ["nav"]

    text = combine_markdown_files(docs_root)

    temp_dir = "./epubs"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    with open(os.path.join(temp_dir, "comb.md"), "w", encoding="utf-8") as f:
        f.write(text)
    split_markdown_by_headings(os.path.join(temp_dir, "comb.md"), temp_dir)
    temp_files = os.listdir(temp_dir)
    temp_files.sort(key=natural_keys)
    i = 1
    for file in temp_files:
        if file != "comb.md" and file.endswith(".md"):
            with open(os.path.join(temp_dir, file), "r", encoding="utf-8") as f:
                content = f.read()
                html_content = markdown2.markdown(content, extras=["tables"])
                # with open("./epubs/{file}.html", "w", encoding='utf-8') as f:
                #     f.write(html_content)
                print(f"{file} Md2Html finished")
                chapter = epub.EpubHtml(
                    title=f"{os.path.splitext(file)[0]}",
                    file_name=f"chap_{i}.xhtml",
                    content=html_content,
                )
                i += 1
                epub_book.add_item(chapter)
                epub_book.toc.append(chapter)
                spine.append(chapter)
                print(f"{file} added")

    for file in temp_files:
        if file.endswith(".md"):
            os.remove(os.path.join(temp_dir, file))
    copy_assets_epub("./docs", epub_book)

    epub_book.spine = spine
    epub_book.add_item(epub.EpubNcx())
    epub_book.add_item(epub.EpubNav())
    epub.write_epub(output_epub, epub_book)
    print("Epub generated!")


if __name__ == "__main__":
    root_directory = "./docs"  # Replace with your root directory
    output_epub_file = "./Palladium_Fantasy_zh_Hans.epub"

    md2epub(root_directory, output_epub_file)
