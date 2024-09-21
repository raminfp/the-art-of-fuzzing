#### CodeQL tutorial


####### Download CodeQL:
```bash
$ git clone --depth=1 https://github.com/github/codeql.git queries
```

####### Download CodeQL-cli:
```bash
$ wget https://github.com/github/codeql-cli-binaries/releases/download/v2.5.5/codeql-linux64.zip # https://github.com/github/codeql-cli-binaries/releases
```

###### Download Applicatoin:
```bash
$ cd ./app_scan
$ git clone --depth=1 https://github.com/DevSlop/Pixi.git Pixi

```

###### Create Database:
```bash
$ codeql database create \
  ./databases/Pixi \
  --language="javascript" \
  --source-root="./apps/Pixi"
```

###### CodeQL Analysing 
```bash
$ codeql database analyze \
  --format="csv" \
  --output="./results/xss-reflected.csv" \
  ./databases/Pixi \
  ./queries/javascript/ql/src/Security/CWE-079/ReflectedXss.ql
```