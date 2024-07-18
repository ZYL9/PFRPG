import { defineConfig } from "vitepress";
import { withPwa } from "@vite-pwa/vitepress";
// import { SearchPlugin } from "vitepress-plugin-search";
import { chunkSplitPlugin } from 'vite-plugin-chunk-split';
// import viteCompression from 'vite-plugin-compression';
import { generateSidebar } from 'vitepress-sidebar';

// import { sidebarData } from "./sidebar.js";


//现在使用flex-search,找到了minisearch新的解决方案，效果比这个好
// 载入模块
// var Segment = require('segment');
// import Segment from 'segment'
// 创建实例
// var segment = new Segment();
// 使用默认的识别模块及字典，载入字典文件需要1秒，仅初始化时执行一次即可
// segment.useDefault();
// var searchOptions = {

//   //采用分词器优化，解决汉字搜索问题。效果和大小折中
//   //来源：https://github.com/emersonbottero/vitepress-plugin-search/issues/11
//   encode: function (str) {
//     return segment.doSegment(str, { simple: true });
//   },
//   tokenize: "foward",

//   // 以下代码返回完美的结果，但内存与空间消耗巨大
//   // encode: false,
//   // tokenize: "full",

//   //官方推荐方法，不是很理想，留作备用
//   // encode: false,
//   // tokenize: function (str) {
//   //   return segment.doSegment(str, { simple: true });
//   // }
//   // encode: str => str.replace(/[\x00-\x7F]/g, "").split("")
// };

//用于压缩，cfpages已经自动用了，如果自己部署需要打开
// var compressOptions = {
//   verbose: true,
//   disable: false,
//   threshold: 1024,
//   algorithm: "brotliCompress",
//   ext: ".br",
// }
const vitepressSidebarOptions =
{
  /*
   * For detailed instructions, see the links below:
   * https://vitepress-sidebar.jooy2.com/guide/api
   */
  documentRootPath: '/docs',
  // scanStartPath: null,
  // resolvePath: null,
  // useTitleFromFileHeading: true,
  useTitleFromFrontmatter: true,
  // frontmatterTitleFieldName: 'title',
  // useFolderTitleFromIndexFile: false,
  useFolderLinkFromIndexFile: true,
  // hyphenToSpace: true,
  // underscoreToSpace: true,
  // capitalizeFirst: false,
  // capitalizeEachWords: false,
  collapsed: true,
  // collapseDepth: 2,
  // sortMenusByName: false,
  // sortMenusByFrontmatterOrder: false,
  // sortMenusByFrontmatterDate: false,
  // sortMenusOrderByDescending: false,
  // sortMenusOrderNumericallyFromTitle: true,
  sortMenusOrderNumericallyFromLink: true,
  // frontmatterOrderDefaultValue: 0,
  // manualSortFileNameByPriority: ['first.md', 'second', 'third.md'],
  // removePrefixAfterOrdering: false,
  // prefixSeparator: '.',
  // excludeFiles: ['first.md', 'secret.md'],
  excludeFilesByFrontmatterFieldName: 'exclude',
  // excludeFolders: ['secret-folder'],
  // includeDotFiles: false,
  // includeRootIndexFile: false,
  // includeFolderIndexFile: false,
  // includeEmptyFolder: false,
  // rootGroupText: 'Contents',
  // rootGroupLink: 'https://github.com/jooy2',
  // rootGroupCollapsed: false,
  // convertSameNameSubFileToGroupIndexPage: false,
  // folderLinkNotIncludesFileName: false,
  // keepMarkdownSyntaxFromTitle: false,
  // debugPrint: false,
}

// https://vitepress.dev/reference/site-config
export default withPwa(
  defineConfig({
    title: "钯界传奇",
    head: [["link", { rel: "icon", href: "/favicon.ico" }]],
    description: "Palladium Fantasy",
    themeConfig: {
      // https://vitepress.dev/reference/default-theme-config
      logo: "/logo.webp",
      nav: [
        { text: "Home", link: "/" },
        { text: "Docs", link: "/C01-创建角色/1.1第一步：八属性与属性加值.md" },
        { text: "About", link: "/0.关于.md" },
      ],

      socialLinks: [{ icon: "github", link: "https://github.com/ZYL9/PFRPG" }],
      outline: {
        level: [1, 3],
      },
      search: {
        provider: "local",
        options: {
          miniSearch: {
            options: {
              tokenize: (term) => {
                if (typeof term === 'string') term = term.toLowerCase();
                // @ts-ignore
                const segmenter = Intl.Segmenter && new Intl.Segmenter("zh", { granularity: "word" });
                if (!segmenter) return [term];
                const tokens = [];
                for (const seg of segmenter.segment(term)) {
                  // @ts-ignore
                  tokens.push(seg.segment);
                }
                return tokens;
              },
            },
            searchOptions: {
              combineWith: 'AND', // important for search chinese
              processTerm: (term) => {
                if (typeof term === 'string') term = term.toLowerCase();
                // @ts-ignore
                const segmenter = Intl.Segmenter && new Intl.Segmenter("zh", { granularity: "word" });
                if (!segmenter) return term;
                const tokens = [];
                for (const seg of segmenter.segment(term)) {
                  // @ts-ignore
                  tokens.push(seg.segment);
                }
                return tokens;
              },
            },
          },
        },
      },
      editLink: {
        pattern: "https://github.com/ZYL9/PFRPG/edit/main/docs/:path",
        text: "Edit this page on GitHub",
      },
      sidebar: generateSidebar(vitepressSidebarOptions)
    },
    markdown: {
      image: {
        // 图片懒加载
        lazyLoading: true
      }
    },
    ignoreDeadLinks: true,
    metaChunk: true,
    lang: "zh-cn",
    vite: {
      plugins: [
        // SearchPlugin(searchOptions),//使用flex-search,找到了minisearch新的解决方案，效果比这个好
        chunkSplitPlugin(),
        // viteCompression(compressOptions)//用于压缩，cfpages已经自动用了，如果自己部署需要打开

      ],
    },
    pwa: {
      includeAssets: ["favicon.ico"],
      workbox: {
        globPatterns: ["**/*.{css,js,html,jpg,svg,png,ico,webp,txt,woff2}"],
      },
      manifest: {
        name: "钯界传奇",
        short_name: "钯界传奇",
        description: "Palladium Fantasy",
        theme_color: "#ffffff",
        icons: [
          {
            src: "logo192.webp",
            sizes: "192x192",
            type: "image/webp",
          },
          {
            src: "logo512.webp",
            sizes: "512x512",
            type: "image/webp",
          },
        ],
      },
    },
  })
);
