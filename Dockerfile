# ---- Base Node ----
FROM node:lts-alpine3.19 AS base
# 创建 app 目录
WORKDIR /app

# ---- Dependencies ----
FROM base AS dependencies  
# 使用通配符复制 package.json 与 package-lock.json
COPY package*.json ./
# 安装在‘devDependencies’中包含的依赖
#公网测试用阿里的npm源
#RUN npm install -g pnpm --registry=https://registry.npmmirror.com
#RUN pnpm install --registry=https://registry.npmmirror.com
#腾讯云上用内网腾讯npm源
RUN npm install -g pnpm --registry=http://mirrors.tencentyun.com/npm/
RUN pnpm install --registry=http://mirrors.tencentyun.com/npm/

# ---- Build ----
FROM dependencies AS build  
WORKDIR /app
COPY ./ /app
RUN node generate-sidebar.js
RUN pnpm vitepress build docs

# ---- Prod ----
FROM nginx:stable-alpine-slim as prod
COPY --from=build /app/docs/.vitepress/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]