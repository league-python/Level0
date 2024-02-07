# Level0

Level 0 Recipes in Github Pages format


## Setup and run 

Install the lesson plan program 
```bash 
pip ihttps://github.com/league-infrastructure/lesson-builder.git#egg=lesson-builder
```

Install vuepress, [see these instructions for details. ](https://vuepress.vuejs.org/guide/getting-started.html). Then create a new vuepress project:

```bash
yarn create vuepress-site && (cd docs && yarn install)
```

If you want to deploy to github pages with `jtl deploy`, the `doc` directory must be in a repo that has an 
origin at Github. 


Get a lesson plan repo from github, or create a new one. 


Run the development server. This assumes that the website is in the `docs` directory
    
```bash
./jtl serve
```


Build new pages from the lesson-plan.yml file

```bash
jtl -vv build -l lessons -d docs -a ~/proj/league-projects/curriculum/
```


Deploy the site to github pages. Note that deploy will only work if the `docs` directory is in a github repo, and the repo is set to produce web pages from the root of the gh-pages branch

```bash
./jtl deploy
```


NOTE: the `base:` key in the lessons plan `config.yml` file  must be the directory below the doman in the URL of your Github page, so if the repo name is 'Level0', then `config.yaml` must have `base: /Level0/`


If you get a bunch of nasty errors, you may need to work around a bud with OpenSSL and Node 17:

``bash
NODE_OPTIONS=--openssl-legacy-provider ./jtl deploy
```