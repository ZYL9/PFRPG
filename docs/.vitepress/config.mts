import { defineConfig } from "vitepress";
import { withPwa } from "@vite-pwa/vitepress";
import sidebar from "./sidebar";

// https://vitepress.dev/reference/site-config
export default withPwa(
  defineConfig({
    title: "钯界传奇",
    head: [["link", { rel: "icon", href: "favicon.ico" }]],
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
      search: {
        provider: "local",
      },
      editLink: {
        pattern: "https://github.com/ZYL9/PFRPG/edit/main/docs/:path",
        text: "Edit this page on GitHub",
      },
      sidebar,
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
