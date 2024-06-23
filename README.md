# SotDL

init
```sh
# auto spilt markdown file
cd ./origin
python spilter.py
```

deploy
```sh
# generate sidebar file
pnpm run prebuild
# vitepress build
pnpm run build
```

support docker
need to change npm source
```sh
docker run build .
```