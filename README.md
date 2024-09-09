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

### deploy
```sh
# vitepress build
pnpm run build
# output file in ./docs/.vitepress/dist
# serve
pnpm run preview
```

support docker(Not recommend)
```sh
docker run build .
```

compile to epub(Not recommend, should use pandoc instead)
```sh
pip install markdown2 ebooklib
python md2pub.py
```
