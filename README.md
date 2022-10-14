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
cd twint && pip3 install . -r requirements.txt
```

## Example Usage

```
$ twint -s "Donald Trump" --since 2022-01-01 --until 2022-09-01
```
