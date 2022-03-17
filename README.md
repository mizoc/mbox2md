# mbox2txt
Convert mbox file to txt

## Installtion
```bash
$git clone https://github.com/mizoc/mbox2txt
$pip install -r ./requirements.txt
```

## Usage
```bash
# One file per one mail
$python3 ./convert2respective_md.py IN.mbox && nkf -Lu -w --overwrite out/*

# combine in a single file
$python3 ./convert.py IN.mbox >OUT.txt`  
```
