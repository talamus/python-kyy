# Kyy

A Finnish language variant of the Python programming language.

### An example

A Kyy program:
```
eläimet = ["kissa", "karhu", "koira"]

jokaiselle sijainnille, eläimelle joka löytyy numeroiduista(eläimistä):
    jos sijainti > 1:
        tulosta(f"Tosi iso {eläin}")
    muuten:
        tulosta(sijainti, eläin)
```

Translates into Python program:
```
eläin_plural = ["kissa", "karhu", "koira"]

for sijainti, eläin in enumerate(eläin_plural):
    if sijainti > 1:
        print(f"Tosi iso {eläin}")
    else:
        print(sijainti, eläin)
```

### Installation and dependencies

#### 1. Make sure that a Finnish language Voikko is installed

```
$ sudo apt install libvoikko1 voikko-fi
```

#### 2. Install Poetry according to package instructions

https://python-poetry.org/docs/#installation

#### 3. Clone repository and initialize virtual environment

```
$ git clone git@github.com:talamus/python-kyy.git
$ cd python-kyy
$ poetry shell
$ poetry update
```

#### 3. Go and have fun!

```
$ python -m kyy examples/eläimet.kyy
0 kissa
1 karhu
Tosi iso koira

$ python -m kyy --help
usage: python -m kyy [-h] [-o [program.py]] [-n] [-v] [program.kyy]

A Finnish language variant of the Python programming language.

positional arguments:
  program.kyy           the program file to be executed; defaults to stdin

options:
  -h, --help            show this help message and exit
  -o [program.py], --output-python [program.py]
                        output python source code
  -n, --no-exec         don't execute the program
  -v, --verbose         be more verbose
```
