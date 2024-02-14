print("[read_reports] importing library")
import os
import io

# Read example text files from the directory
# Example text reports (replace with your own data)
def read_all(dirname, endswith):
    reports = []
    for filename in os.listdir(dirname):
        if filename.endswith(endswith):
            with io.open(os.path.join(dirname, filename), 'r', encoding='utf8') as f:
                reports.append([line.strip() for line in f])
    #print(reports)
    return(reports)
