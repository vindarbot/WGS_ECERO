#! python
import os
import sys
import subprocess 

from multiprocessing import Pool

def process_pair(fileR1):
    dividing = fileR1.split(".")
    if "R1" in fileR1:
        fileR2 = fileR1.replace('R1', 'R2')
        if os.path.isfile(inputdirectory + fileR2):
            dividing1 = fileR2.split(".")
            log1 = dividing[0]
            output = dividing[0].split('R1')[0].rstrip('_')
            output2 = dividing1[0]
            subprocess.call("spades.py -o assembly/" + output + " --pe-1 1 " +
                            inputdirectory + fileR1 + " --pe-2 1 " +
                            inputdirectory + fileR2 +
                            " --pe-or 1 fr --cov-cutoff auto --isolate 2>&1", shell=True)

if __name__ == "__main__":
    inputdirectory = sys.argv[1]
    file_list = [file for file in os.listdir(inputdirectory) if "R1" in file]

    # Adjust the number of processes based on your system's capabilities
    num_processes = 45  # You can change this number as needed

    with Pool(num_processes) as pool:
        pool.map(process_pair, file_list)


