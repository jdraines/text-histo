#!/usr/bin/env python3

import argparse
import os
import collections
from typing import List, Dict, Union, Tuple
import math
import sys


def load_data(file_path: str) -> List[str]:
    """Load data from a text file, one item per line."""
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def count_frequencies(data: List[str]) -> Dict[str, int]:
    """Count the frequency of each item in the list."""
    return dict(collections.Counter(data))


def is_numeric_data(data: List[str]) -> bool:
    """Check if all data items are numeric (integers)."""
    try:
        [int(item) for item in data]
        return True
    except ValueError:
        return False


def create_bins(data: List[int], num_bins: int) -> Tuple[List[Tuple[int, int]], Dict[Tuple[int, int], int]]:
    """
    Create bins for numeric data and count items in each bin.
    
    Returns:
        Tuple containing:
        - List of bin ranges (min, max)
        - Dictionary mapping bin ranges to counts
    """
    min_val = min(data)
    max_val = max(data)
    bin_size = math.ceil((max_val - min_val + 1) / num_bins)
    
    # Create bins
    bins = []
    for i in range(num_bins):
        bin_min = min_val + (i * bin_size)
        bin_max = min_val + ((i + 1) * bin_size - 1) if i < num_bins - 1 else max_val
        bins.append((bin_min, bin_max))
    
    # Count items in each bin
    bin_counts = {bin_range: 0 for bin_range in bins}
    for val in data:
        for bin_range in bins:
            if bin_range[0] <= val <= bin_range[1]:
                bin_counts[bin_range] += 1
                break
    
    return bins, bin_counts


def display_histogram(
    data: Union[Dict[str, int], Dict[Tuple[int, int], int]],
    title: str,
    block_char: str = "█",
    width: int = 50,
    binned: bool = False,
    show_counts_column: bool = False,
    show_counts_in_bars: bool = False
) -> None:
    """Display a text-based histogram."""
    if not data:
        print("No data to display.")
        return

    max_count = max(data.values())
    scale_factor = width / max_count if max_count > 0 else 0
    
    # Calculate the width needed for labels
    if binned:
        max_label_width = max(len(f"{bin_min}-{bin_max}") for bin_min, bin_max in data.keys())
    else:
        max_label_width = max(len(str(item)) for item in data.keys())
    
    # Print title
    header_width = max_label_width + width + (12 if show_counts_column else 2)
    print(f"\n{title}\n{'=' * header_width}")
    
    # Build header line based on options
    header = f"{'Value':<{max_label_width}} |"
    if show_counts_column:
        header += f" {'Counts':<10} |"
    header += " Histogram"
    print(header)
    
    # Build separator line
    separator = f"{'-' * max_label_width}-+"
    if show_counts_column:
        separator += f"{'-' * 12}+"
    separator += f"{'-' * (width + 1)}"
    print(separator)
    
    # Sort items for display
    if binned:
        # Sort bins by their lower bound
        sorted_items = sorted(data.items(), key=lambda x: x[0][0])
    else:
        # Try to sort numerically if possible, otherwise sort alphabetically
        try:
            sorted_items = sorted(data.items(), key=lambda x: (int(x[0]), x[0]))
        except ValueError:
            sorted_items = sorted(data.items())
    
    # Print each row
    for item, count in sorted_items:
        if count == 0 and binned:
            continue  # Skip empty bins
            
        # Format the label based on whether we're using bins or not
        if binned:
            bin_min, bin_max = item
            label = f"{bin_min}-{bin_max}"
        else:
            label = str(item)
        
        bar_length = int(count * scale_factor)
        bar = block_char * bar_length
        
        # Add count at the end of the bar if requested
        if show_counts_in_bars and bar_length > 0:
            bar = bar + f" {count}"
        
        # Build the row based on options
        row = f"{label:<{max_label_width}} |"
        if show_counts_column:
            row += f" {count:<10} |"
        row += f" {bar}"
        
        print(row)


def process_file(file_path, bins=10, char="█", width=50, no_binning=False, 
                show_counts_column=False, show_counts_in_bars=False):
    """Process a file and generate a histogram."""
    # Load data
    data = load_data(file_path)
    if not data:
        print(f"No data found in {file_path}")
        return
    
    # Extract title from filename (without path and extension)
    title = os.path.splitext(os.path.basename(file_path))[0]
    
    # Check if data is numeric for potential binning
    if is_numeric_data(data) and not no_binning:
        numeric_data = [int(item) for item in data]
        _, bin_counts = create_bins(numeric_data, bins)
        display_histogram(
            bin_counts, 
            title, 
            char, 
            width, 
            binned=True, 
            show_counts_column=show_counts_column,
            show_counts_in_bars=show_counts_in_bars
        )
    else:
        # Use regular frequency counting
        frequencies = count_frequencies(data)
        display_histogram(
            frequencies, 
            title, 
            char, 
            width, 
            binned=False,
            show_counts_column=show_counts_column,
            show_counts_in_bars=show_counts_in_bars
        )


def main(args=None):
    """Main entry point for the CLI."""
    if args is None:
        args = sys.argv[1:]
        
    parser = argparse.ArgumentParser(description="Generate a text-based histogram from data in a file.")
    parser.add_argument("file", help="Path to the input file")
    parser.add_argument("--bins", type=int, default=10, help="Number of bins for numeric data (default: 10)")
    parser.add_argument("--char", default="█", help="Character(s) used to draw histogram bars (default: █)")
    parser.add_argument("--width", type=int, default=50, help="Width of the histogram in characters (default: 50)")
    parser.add_argument("--no-binning", action="store_true", help="Disable automatic binning for numeric data")
    parser.add_argument("--counts-col", action="store_true", help="Show counts column in output (hidden by default)")
    parser.add_argument("--counts", action="store_true", help="Show count values at the end of histogram bars")
    
    parsed_args = parser.parse_args(args)
    
    process_file(
        parsed_args.file,
        bins=parsed_args.bins,
        char=parsed_args.char,
        width=parsed_args.width,
        no_binning=parsed_args.no_binning,
        show_counts_column=parsed_args.counts_col,
        show_counts_in_bars=parsed_args.counts
    )


if __name__ == "__main__":
    main()