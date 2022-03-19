# mbox2md
Convert mbox file to markdown files(One file per one mail)

## Installtion
```bash
$git clone https://github.com/mizoc/mbox2md
$cd $_
$mkdir {out,attachments}
$pip install -r ./requirements.txt
```

## Usage
```bash
$python3 ./convert.py IN.mbox && nkf -Lu -w --overwrite out/*
#Then, cat out/*.md
```
