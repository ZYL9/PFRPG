# convert_to_epub.py
import os
import markdown2
from ebooklib import epub


def convert_markdown_to_epub(input_dir, output_file):
    # Create EPUB book
    book = epub.EpubBook()
    book.set_title("Documentation")
    book.set_language("en")

    chapters = []

    for root, _, files in os.walk(input_dir):
        for file in sorted(files):
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                relpath = os.path.relpath(filepath, input_dir)
                chapter_title = os.path.splitext(relpath)[0].replace(os.path.sep, " - ")

                # Read markdown file
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                # Convert markdown to HTML
                html = markdown2.markdown(content)

                # Create chapter
                chapter = epub.EpubHtml(
                    title=chapter_title,
                    file_name=f"{chapter_title}.xhtml",
                    content=html,
                )
                book.add_item(chapter)
                chapters.append(chapter)

    # Set the spine and the table of contents
    book.spine = ["nav"] + chapters
    book.toc = tuple(chapters)

    # Write the EPUB file
    epub.write_epub(output_file, book)


if __name__ == "__main__":

    inputDir = "./docs"
    outputDir = "./epubs/output.epub"

    convert_markdown_to_epub(inputDir, outputDir)
