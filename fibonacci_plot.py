#!/usr/bin/env python3
"""
Generate a Fibonacci-like sequence starting with 2 and plot it.
Each new number is the sum of the current and previous number.
"""

import matplotlib.pyplot as plt
import numpy as np

def generate_sequence(iterations=1_000):
    """
    Generate a Fibonacci-like sequence starting with 2.
    Each new number = current number + previous number.

    Args:
        iterations: Number of iterations to run

    Returns:
        List of sequence values
    """
    # Start with 2, 2
    prev = 2
    current = 2
    sequence = [prev, current]

    # Generate the sequence
    for _ in range(iterations - 2):
        next_val = current + prev
        sequence.append(next_val)
        prev = current
        current = next_val

    return sequence

def main():
    print("Generating Fibonacci-like sequence starting with 2...")
    print("Running 1000 iterations...")

    sequence = generate_sequence(1_000)

    print(f"Sequence generated with {len(sequence)} values")
    print(f"First 10 values: {sequence[:10]}")
    print(f"Last value: {sequence[-1]}")

    # Plot the sequence
    print("Creating plot...")
    plt.figure(figsize=(12, 6))
    plt.plot(sequence, color='blue', linewidth=0.5)
    plt.title('Fibonacci-like Sequence (Starting with 2)', fontsize=14)
    plt.xlabel('Iteration', fontsize=12)
    plt.ylabel('Value', fontsize=12)
    plt.grid(True, alpha=0.3)

    # Use log scale for y-axis since values grow exponentially
    plt.yscale('log')

    # Save the plot
    plt.savefig('fibonacci_plot.png', dpi=150, bbox_inches='tight')
    print("Plot saved as 'fibonacci_plot.png'")

    # Show the plot
    plt.show()

if __name__ == "__main__":
    main()
