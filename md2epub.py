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
    lines = content.split('\n')
    adjusted_lines = []
    for line in lines:
        if line.startswith('#'):
            # Count the number of leading '#' characters
            heading_level = 0
            while heading_level < len(line) and line[heading_level] == '#':
                heading_level += 1
            # Adjust the heading level
            new_level = heading_level + level_offset
            if new_level > 6:
                # Convert to bold text if heading level exceeds 6
                bold_text = line[heading_level:].strip()
                adjusted_lines.append(f'**{bold_text}**')
            else:
                adjusted_heading = '#' * new_level + line[heading_level:]
                adjusted_lines.append(adjusted_heading)
        else:
            adjusted_lines.append(line)
    return '\n'.join(adjusted_lines)


def combine_markdown_files(root_dir):
    combined_content = []

    for current_path, dirs, files in os.walk(root_dir):
        # Sort files to ensure index.md is processed first if present
        files = sorted(files, key=lambda f: (f != 'index.md', f))
        level_offset = current_path[len(root_dir):].count(os.sep)

        # Process index.md first if it exists in the directory
        if 'index.md' in files:
            index_path = os.path.join(current_path, 'index.md')
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
                content = remove_yaml_front_matter(content)
                if len(content) > 0:
                    adjusted_content = adjust_heading_levels(content, level_offset - 1)
                    combined_content.append("<hr>")
                    combined_content.append(adjusted_content)
                    combined_content.append("<hr>")
                    combined_content.append("<div STYLE=\"page-break-after: always;\"></div>")

        # Process other markdown files
        for file in files:
            if file != 'index.md' and file.endswith('.md'):
                file_path = os.path.join(current_path, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    content = remove_yaml_front_matter(content)
                    adjusted_content = adjust_heading_levels(content, level_offset)
                    combined_content.append("<hr>")
                    combined_content.append(adjusted_content)
                    combined_content.append("<hr>")
                    combined_content.append("<div STYLE=\"page-break-after: always;\"></div>")

    return '\n'.join(combined_content)


def copy_assets_epub(src_dir, epub_book):
    asset_id = 1
    for current_path, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.webp'):
                image_content = open(os.path.join(current_path, file), 'rb').read()
                img = epub.EpubImage(uid=f'image_{asset_id}',
                                     file_name='./assets/' + file,
                                     content=image_content)
                asset_id = asset_id + 1
                epub_book.add_item(img)
    print(f"Total {asset_id} image added")


def md2epub(docs_root, output_epub):
    epub_book = epub.EpubBook()
    epub_book.set_title("Palladium_Fantasy_zh_Hans")
    epub_book.set_language("zh-Hans")
    epub_book.add_author("Author Name")
    epub_book.set_cover("cover.webp", open("./docs/public/cover.webp", "rb").read())

    text = combine_markdown_files(docs_root)
    html_content = markdown2.markdown(text, extras=["tables"])
    with open("./epubs/raw.html", "w", encoding='utf-8') as f:
        f.write(html_content)
    print("Md2Html finished")
    chapter = epub.EpubHtml(
        title="Palladium_Fantasy_zh_Hans",
        file_name=f"full.xhtml",
        content=html_content,
    )
    epub_book.add_item(chapter)
    print("Text added")

    copy_assets_epub("./docs", epub_book)

    epub_book.spine = ["nav", chapter]
    epub_book.add_item(epub.EpubNcx())
    epub_book.add_item(epub.EpubNav())
    epub.write_epub(output_epub, epub_book)
    print("Epub generated!")


if __name__ == "__main__":
    root_directory = "./docs"  # Replace with your root directory
    output_epub_file = "./epubs/Palladium_Fantasy_zh_Hans.epub"

    md2epub(root_directory, output_epub_file)
