import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py databases/large.csv sequences/5.txt")

    # Read database file into a variable
    with open(sys.argv[2], 'r') as dna_file:
        dna = dna_file.read()

    # create a sequence as a dict with people's information
    sequences = {}
    # Read DNA sequence file into a variable
    dna_sequence = sys.argv[1]
    with open(dna_sequence) as people_dna:
        reader = csv.reader(people_dna)
        for row in reader:
            DNAsequence = row
            # extract the sequences from the DNA database into a list
            DNAsequence.pop(0)
            # copy this list into a dictionary
            for item in DNAsequence:
                sequences[item] = 0
            break

    # Find longest match of each STR in DNA sequence
    for key in sequences:
        ans = longest_match(dna, key)
        sequences[key] += ans

    # Check database for matching profiles
    with open(sys.argv[1], "r") as people_file:
        people = csv.DictReader(people_file)
        for person in people:
            match = 0
            for key in sequences:
                if int(person[key]) == sequences[key]:
                    match += 1
            if match == len(sequences):
                print(person["name"])
                exit(0)
        print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0
        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:
            
            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
