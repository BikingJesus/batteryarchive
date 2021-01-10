# Batteryarchive
The repository contains scripts to interact with www.batteryarchive.org.

Battery Archive (BA) is a repository for easy visualization, analysis, and comparison of battery data across institutions. It is based on an instance of redash (https://github.com/getredash/redash).

The file metadata.csv contains cell_ids and metadata for the cells in the archive.

The script datatransfer.py can be used to download data from battery archive. To run the script:

python3 datatransfer.py

The script will attempt to download two types of files.

1. [cell_id]_cycle_data.csv
2. [cell_id]_timeseries.csv

The first file contains cycle quantities. The second file contains time-series data. The files are downloaded to the directory that contains the python file.

More details about the list of studies can be found online:

https://batteryarchive.org/study_summaries.html

For questions, email info@batteryarchive.org.
