import sys
import csv

def main():
    """
    Function to overwrite visualisation_settings.csv.

    Pre
    ---
    Must get Holland or Nationaal as map and a relative path from 
    TijeJonaFinn/parent/code to a properly formatted csv output file to 
    make Manim visualisation work properly.

    Post
    ---
    Overwrites visualisation_settings.csv to make manim visualisation 
    automated.

    Example Usage
    python3 set_manim_settings.py "Nationaal" "autorun_hillclimber/maandagnacht_Nationaal_Jona_3/solutions/Nationaal_6530_HC.csv"
    ---
    """

    # Check amount of arguments correct
    if len(sys.argv) != 3:
        raise ValueError("Usage: python3 set_manim_settings.py <map> <pad>")

    # Overwrite visualisation_settings.csv
    with open('visualisation_settings.csv', newline = '', mode = 'w') as file:
        writer = csv.writer(file)
        writer.writerow([sys.argv[1],sys.argv[2]])

if __name__ == "__main__":
    main()