#### Bym
**Bym** is a web folder/files disovery script, I'm still working on that, but so soon this code will be 100% functional.

**Default Scanning**
```shell
python3 bym.py -u https://target.com
```

**Saving Output Result**
```shell
python3 bym.py -u https://target.com -o result.txt
```

**Set a Random Delay Between Request** - In order to bypass WAF
```shell
python3 bym.py -u http://target.com -t R -o result.txt
```

**Tracking Files on the Target**
```shell
python3 bym.py -u http://target.com -f php,sql,db -t R -o result.txt
```
