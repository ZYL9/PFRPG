import { defineConfig } from "vitepress";
import { withPwa } from "@vite-pwa/vitepress";
import { SearchPlugin } from "vitepress-plugin-search";
import { chunkSplitPlugin } from 'vite-plugin-chunk-split';

import { sidebarData } from "./sidebar.js";

// 载入模块
// var Segment = require('segment');
import Segment from 'segment'
// 创建实例
var segment = new Segment();
// 使用默认的识别模块及字典，载入字典文件需要1秒，仅初始化时执行一次即可
segment.useDefault();

var options = {

  // 采用分词器优化，
  encode: function (str) {
    return segment.doSegment(str, { simple: true });
  },
  tokenize: "foward",
  // // 解决汉字搜索问题。来源：https://github.com/emersonbottero/vitepress-plugin-search/issues/11


  // 以下代码返回完美的结果，但内存与空间消耗巨大，索引文件达到80M+
  // encode: false,
  // tokenize: "full",

  // encode: false,
  // tokenize: function (str) {
  //   return segment.doSegment(str, { simple: true });
  // }
};

// https://vitepress.dev/reference/site-config
export default withPwa(
  defineConfig({
    title: "钯界传奇",
    head: [["link", { rel: "icon", href: "/favicon.ico" }]],
    description: "Palladium Fantasy",
    themeConfig: {
      // https://vitepress.dev/reference/default-theme-config
      logo: "/logo.png",
      nav: [
        { text: "Home", link: "/" },
        { text: "Docs", link: "/C01-创建角色/1.1第一步：八属性与属性加值.md" },
        { text: "About", link: "/0.关于.md" },
      ],

      socialLinks: [{ icon: "github", link: "https://github.com/ZYL9/PFRPG" }],
      outline: {
        level: [1, 3],
      },
      // search: {
      //   provider: "local",
      // },
      editLink: {
        pattern: "https://github.com/ZYL9/PFRPG/edit/main/docs/:path",
        text: "Edit this page on GitHub",
      },
      sidebar: sidebarData,
    },
    ignoreDeadLinks: true,
    metaChunk: true,
    lang: "zh-cn",
    vite: {
      plugins: [
        SearchPlugin(options),
        chunkSplitPlugin()
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
            src: "logo192.png",
            sizes: "192x192",
            type: "image/png",
          },
          {
            src: "logo512.png",
            sizes: "512x512",
            type: "image/png",
          },
        ],
      },
    },
  })
);
