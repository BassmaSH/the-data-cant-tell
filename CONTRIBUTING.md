# Contributing

Fourteen guidelines for the code in this repo, and how each one is checked. They follow Google's
Python Style Guide, "Good Enough Practices in Scientific Computing" (Wilson et al., 2017), the Good
Research Code Handbook and the ML Code Completeness Checklist. They are the same as in
[eval-flagged-payments](https://github.com/BassmaSH/eval-flagged-payments), adapted to the files
here.

## Before you push

```bash
pip install ruff==0.17.5 pytest
ruff format .                          # rewrites the files in the agreed style
ruff check .                           # reports what breaks a rule
pytest -q                              # 63 checks, no API call, no key
python grading/2026-10-20/combine.py   # the published tables, rebuilt from the grading files
python data/check_data.py              # the nine planted episodes, recomputed from the database
```

The same steps run on every push (`.github/workflows/check.yml`), followed by a rebuild of the
database and of the data blocks, which must change no file. The settings are in `pyproject.toml`.
None of these steps calls a model. Only `run_cases.py` does, and no check runs it.

## The guidelines

| # | guideline | checked by |
|---|---|---|
| 1 | One job per function, about 40 lines at most | ruff: 40 statements, 10 branches, 6 arguments |
| 2 | A choice between named things is a table, not an `if` chain (`SETUPS` in `run_cases.py`, `FILES` and `SETUP_TAG` in `combine.py`, `MAKERS`, `COMPUTE`) | review |
| 3 | Nothing runs at import: every script has a `main()`, and a client or a database is opened on first use | review; the tests import every script |
| 4 | Each piece of logic lives in one place | review |
| 5 | A file opens with what it does, how to run it, and who wrote it | ruff: a docstring is required |
| 6 | Comments say why, never what | review |
| 7 | Every rule behind a published number has a test | review; the tests run on every push |
| 8 | A formatter and a linter decide style | ruff, 100 characters |
| 9 | Computing is kept apart from reading and writing files | review |
| 10 | No state shared between functions behind their backs | ruff flags `global`; review |
| 11 | Numbers, columns and paths have names | review |
| 12 | Every table in the README has the command that rebuilds it; dependencies are written down | `combine.py` runs on every push, and a test compares its tables with `README.md` and `NOTEBOOK.md` |
| 13 | Type hints on every function; a docstring with `Args:` and `Returns:` where the names do not say it | ruff |
| 14 | One folder per role; a script sits next to the files it builds | review |

"Review" means a person reads the change against the guideline: no tool checks it.

## Where a file goes

| folder | role | goes here |
|---|---|---|
| root | what a reader runs and reads | `run_cases.py`, `README.md`, `NOTEBOOK.md` (the record of every run) |
| `cases/` | the test itself | one file per case: the question, the right answer, the prediction |
| `cases/data/` | what the model sees | one data block per case, and the two scripts that build them |
| `data/` | the invented company | the database, the script that builds it, the answer key `causes.json` |
| `results/<date>/` | what came out | one file per answer, never edited |
| `grading/<date>/` | the verdicts | one file per model, the brief the graders were given, `combine.py` |
| `tests/` | how the code is checked | one file per script or pair of scripts tested |

## Changing something that produces a number

The numbers in the README come from three places: the answers in `results/`, the verdicts in
`grading/2026-10-20/*.md`, and `grading/2026-10-20/combine.py`, which counts them. A change to any
of them must show that the published numbers still follow:

- `python grading/2026-10-20/combine.py` must print the tables of `README.md` and of
  `NOTEBOOK.md` ("Runs 6 and 7 graded"). `tests/test_combine.py` compares them line by line.
- `python data/make_data.py` must print the content hash written in `data/README.md`
  (`a5447e8fda05733a`), and `python data/check_data.py` must end with "9 of 9".
- `python cases/data/make_case_data.py` and `python cases/data/make_computed.py` must leave every
  file in `cases/data/` unchanged.

Three rules for the records:

- **Saved answers are never replaced.** `run_cases.py` writes to a folder named after the day of
  the run. A new run gets a new folder, and its prediction is written in `NOTEBOOK.md` before it
  is run.
- **A verdict is never edited in place.** To change one, write the cell as `n → y` (the grader's
  verdict, then the one counted), and add the case, the rule and who changed it under "Verdicts
  changed after grading" in the same file. `combine.py` counts the right-hand verdict, and a test
  lists the changed cells, so a new one has to be added to that test too.
- **The notebook, the case files and the grading files are records.** They say "her" for the
  author and are kept as written; a correction is a dated note, not a rewrite. Code comments say
  "the author".

## Not covered

- The verdicts themselves are judgements. The tests check that they are counted right, not that
  they are right.
- The data blocks of C04 and C06 to C09 have no script. `tests/test_case_data.py` compares the
  figures of their first table with the database; their notes, price changes and file lists are
  not compared.
- `run_cases.py` is tested up to the call: which models, which system message, which file names.
  No test calls a model.
- `requirements.txt` gives lower bounds. The versions of the libraries used for the runs of
  October 2026 were not recorded.
