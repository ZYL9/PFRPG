# PFRPG

## Palladium Fantasy RPG® 2nd Edition

**Please support genuine**

https://palladiumbooks.com/fantasy/palladium-fantasy-rpg

## Usage

~~init~~(obsolete)
```sh
# auto spilt markdown file
cd ./origin
python spilter.py
```
--- 

deploy
```sh
# generate sidebar file
pnpm run prebuild
# vitepress build
pnpm run build
```

support docker
need to change npm source/apk source
```sh
docker run build .
```

compile to epub
```sh
pip install markdown2 ebooklib
python md2pub.py
```