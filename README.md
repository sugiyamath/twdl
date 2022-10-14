# twdl

twdl is a twitter scraping tool.

## Requirements
- Python >= 3.6;
- aiohttp;
- aiodns;
- beautifulsoup4;
- cchardet;
- dataclasses
- schedule;
- fake-useragent;

## Installing

```bash
git clone --depth=1 https://github.com/sugiyamath/twdl.git
cd twdl && pip3 install . -r requirements.txt
```

## Example Usage

```
$ twdl -s "Donald Trump" --since 2022-01-01 --until 2022-09-01
```

## Ref
original source: https://github.com/twintproject/twint
