# Text Histogram Generator

A simple Python package for generating text-based histograms from data in text files.

## Features

- Load data from text files (one item per line)
- Count occurrences of items in the list
- Automatic binning for numeric (integer) data
- Customizable histogram character
- Pretty-formatted text output with labels
- Title automatically generated from filename

## Installation

### Using pipx (recommended for CLI tools)

```bash
# Install pipx if you don't have it
pip install pipx
pipx ensurepath

# Install text-histo
pipx install .
```

### Using pip

```bash
pip install .
```

## Usage

Once installed, you can use the tool from the command line:

```
text-histo [options] file
```

### Required Arguments

- `file`: Path to the input file (one item per line)

### Optional Arguments

- `--bins N`: Number of bins for numeric data (default: 10)
- `--char CHAR`: Character(s) used to draw histogram bars (default: █)
- `--width WIDTH`: Width of the histogram in characters (default: 50)
- `--no-binning`: Disable automatic binning for numeric data
- `--counts`: Display counts at the end of the histogram bars
- `--counts-col`: Display counts in a counts column

## Examples

Example files are provided in the `examples` directory.

### Numeric Data with Binning

```
text-histo examples/sample_numeric.txt
```

Output:
```
sample_numeric
=================================================
Value     | Histogram
----------+--------------------------------------------------
12-19     | █
20-27     | ███████
28-35     | ███
36-43     | 
44-51     | ████
52-59     | ███
60-67     | ████
68-75     | 
76-83     | ████
84-91     | ████
```

### Categorical Data

```
text-histo examples/sample_categorical.txt
```

Output:
```
sample_categorical
=================================================
Value     | Histogram
----------+--------------------------------------------------
apple     | ███████████████████████████████████████
banana    | █████████████████████████████████
grape     | ████████████████████
kiwi      | ███████████████
mango     | █████
orange    | █████████████████████████████████
pear      | ██████████
```

### Custom Bar Character

```
text-histo examples/sample_numeric.txt --char "[]"
```

Output will use `[]` instead of `█` for histogram bars.

## Sample Files

Example files are provided in the `examples` directory:

- `examples/sample_numeric.txt`: Contains integer values for testing binning
- `examples/sample_categorical.txt`: Contains fruit names for testing categorical data
