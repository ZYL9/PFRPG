const path = require('path');
const fs = require('fs-extra')

// Function to check if a directory contains any markdown files
function containsMarkdownFiles(dir) {
    const files = fs.readdirSync(dir);
    return files.some(file => {
        const filePath = path.join(dir, file);
        const stats = fs.statSync(filePath);
        return stats.isFile() && path.extname(file) === '.md';
    });
}

function generateStructure(dir) {
    const result = [];

    const files = fs.readdirSync(dir);

    files.forEach(file => {
        const filePath = path.join(dir, file);
        const stats = fs.statSync(filePath);

        if (stats.isDirectory() && containsMarkdownFiles(filePath)) {
            const subItems = generateStructure(filePath);
            const directoryItem = {
                text: file,
                link: `/${path.relative('docs', filePath).replace(/\\/g, '/')}/${file}.md`,
                items: subItems.length > 0 ? subItems : undefined,
                collapsed: true
            };

            const indexFilePath = path.join(filePath, `${file}.md`);
            if (fs.existsSync(indexFilePath)) {
                directoryItem.link = `/${path.relative('docs', indexFilePath).replace(/\\/g, '/')}`;
            } else {
                delete directoryItem.link;
            }

            result.push(directoryItem);
        } else if (stats.isFile() && path.extname(file) === '.md' && path.basename(file, '.md') !== path.basename(dir) && file != "index.md" && file != "about.md") {
            const item = {
                text: path.basename(file, '.md'),
                link: `/${path.relative('docs', filePath).replace(/\\/g, '/')}`,
                collapsed: true
            };
            result.push(item);
        }
    });

    return result;
}

// Main function to generate the file structure for the docs directory
function main() {
    const docsRoot = path.join(__dirname, 'docs');
    const sidebarFile = path.join(__dirname, 'docs/.vitepress/sidebar.js');
    const structure = generateStructure(docsRoot);

    const output = `module.exports = ${JSON.stringify(structure, null, 2)};`;
    fs.writeFileSync(sidebarFile, output);
}

main()
