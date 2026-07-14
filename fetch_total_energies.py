import re
from pathlib import Path

def extract_orca_energies(target_directory=".", output_filename="orca_energies.txt"):
    # Compile the regular expression for faster execution
    orca_energy_rx = re.compile(r"FINAL SINGLE POINT ENERGY\s+([\d\.\-]+)")
    
    results = []
    
    # Recursively find all files ending with .out
    # rglob works like os.walk but is much cleaner with Path objects
    for file_path in Path(target_directory).rglob("*.out"):
        try:
            # Open with errors='ignore' to bypass potential decoding issues in output files
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                match = orca_energy_rx.search(content)
                
                if match:
                    energy_val = match.group(1)
                    # Grabs the immediate parent folder name and the filename (e.g., "job_folder/output.out")
                    folder_and_file = f"{file_path.parent.name}/{file_path.name}"
                    results.append(f"{folder_and_file}: {energy_val}")
                    
        except Exception as e:
            print(f"Could not read {file_path}. Error: {e}")

    # Write all matches to the output text file
    with open(output_filename, "w", encoding="utf-8") as out_file:
        for line in results:
            out_file.write(line + "\n")

    print(f"Extraction finished. {len(results)} matches saved to '{output_filename}'.")

if __name__ == "__main__":
    # Scans the current directory and all subdirectories by default
    extract_orca_energies()