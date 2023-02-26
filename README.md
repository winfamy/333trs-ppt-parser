# Usage Instructions

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

## Todo
- [X] Parse tables in feature output
- [X] Add basic notes parsing
    - [X] Add web scraping
- [ ] Parse bulleted / numbered lists in feature output
- [ ] Add CTS-based PowerPoint files validation
- [ ] Clean up dependencies
- [ ] Document code w/ docstring comments
