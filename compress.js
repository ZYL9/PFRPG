import { promises as fs } from "fs";
import { gzip, brotliCompress } from "zlib";
import { promisify } from "util";
import fg from "fast-glob";

const gzipAsync = promisify(gzip);
const brotliCompressAsync = promisify(brotliCompress);

async function compressFiles() {
    try {
        // 使用 fast-glob 直接获取所有 HTML 文件的路径
        const files = await fg("./docs/.vitepress/dist/**/*.html", { onlyFiles: true });

        for (const file of files) {
            const content = await fs.readFile(file);
            // Gzip
            // const gzipped = await gzipAsync(content);
            // await fs.writeFile(`${file}.gz`, gzipped);
            // Brotli
            const brotlied = await brotliCompressAsync(content);
            await fs.writeFile(`${file}.br`, brotlied);
        }
        console.log("Compression complete.");
    } catch (error) {
        console.error("Error during compression:", error);
    }
}

compressFiles();