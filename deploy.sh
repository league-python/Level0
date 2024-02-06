#!/usr/bin/env sh

# Build a static site and deploy it to Github Pages

# Workaround errors on build due to openssl issues in Node 17
export NODE_OPTIONS=--openssl-legacy-provider

# abort on errors
set -e

# build
cd docs
yarn build

# navigate into the build output directory
cd src/.vuepress/dist 

# if you are deploying to a custom domain
# echo 'www.example.com' > CNAME

git init
git add -A
git commit -m 'deploy'

git push -f https://github.com/league-python/Level0.git master:gh-pages

cd -
