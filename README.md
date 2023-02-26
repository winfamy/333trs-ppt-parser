# Read Me

## Prerequisites
1. Install conda (https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
2. Import conda environment
```bash
conda env create -n <ENVNAME> --file conda-environment.yml
```

## Running
Execute the code using the `python3` command (on Linux, your mileage on Windows machines may vary).
```bash
python3 src/
```

## Usage
This will extract any text from chosen PowerPoint files located in the directory specified. You can choose whether you'd like your output in CSV or JSON. JSON output will attempt to contain more semantic data (bulleted list content, etc) as well as a slide's raw text.
Notes parsing is done with a specific format defined in [src/core/NotesParser.py](src/core/NotesParser.py) under [`SlideNotesParser.labels`](src/core/NotesParser.py#L6). This isn't really well-written and extending it may be an absolute pain. 
Currently, it supports parsing two types from a slide's notes:
1. Lists (with custom separators)
2. Strings

An example PowerPoint that can be used with the notes parsing can be found at [PowerPoint Parser Sample.pptx](reference-files/PowerPoint Parser Sample.pptx).
Its parsed outputs can be found at 
- JSON: [PowerPoint Parser Sample.json](reference-files/PowerPoint Parser Sample.json)
- CSV: [PowerPoint Parser Sample.csv](reference-files/PowerPoint Parser Sample.csv)

## Todo
- [X] Parse tables in feature output
- [X] Add basic notes parsing
    - [X] Add web scraping
- [ ] Parse bulleted / numbered lists in feature output
- [ ] Add CTS-based PowerPoint files validation
- [ ] Clean up dependencies
- [ ] Document code w/ docstring comments
