#!/usr/bin/env bash
# Summary: Roll a chosen number of dice, show each result, and print their total.
# Usage: ./dice.sh <DICE_COUNT> <SIDES>
# Example: ./dice.sh 4 6

show_usage() {
    printf 'Usage: %s <DICE_COUNT> <SIDES>\n' "$0"
    printf 'DICE_COUNT must be 1-100; SIDES must be 1-1000.\n'
    printf 'Use whole numbers without leading zeros. Example: %s 4 6\n' "$0"
}

if [[ $# -eq 1 && $1 == --help ]]; then
    show_usage
    exit 0
fi

if [[ $# -ne 2 ]]; then
    printf 'Error: provide exactly two arguments.\n' >&2
    show_usage >&2
    exit 1
fi

# Check the text and its length before using an argument in arithmetic.
if [[ ! $1 =~ ^[1-9][0-9]{0,2}$ ]] || (( $1 > 100 )); then
    printf 'Error: DICE_COUNT must be a whole number from 1 to 100, without leading zeros.\n' >&2
    exit 1
fi

if [[ ! $2 =~ ^[1-9][0-9]{0,3}$ ]] || (( $2 > 1000 )); then
    printf 'Error: SIDES must be a whole number from 1 to 1000, without leading zeros.\n' >&2
    exit 1
fi

process_rolls() {
    local dice_count=$1
    local sides=$2
    local total=0
    local die random_value value
    local limit=$((32768 - 32768 % sides))

    printf 'Rolling %d dice with %d sides each:\n' "$dice_count" "$sides"

    for ((die = 1; die <= dice_count; die++)); do
        random_value=$RANDOM

        # RANDOM gives 0-32767. Reject the uneven remainder so every side is equally likely.
        while ((random_value >= limit)); do
            random_value=$RANDOM
        done

        value=$((random_value % sides + 1))
        total=$((total + value))
        printf 'Die %d: %d\n' "$die" "$value"
    done

    printf 'Total: %d\n' "$total"
}

process_rolls "$1" "$2"
