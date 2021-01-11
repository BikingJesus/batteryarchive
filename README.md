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

# About the data

We launched Battery Archive to provide battery data and metadata in a standard format that simplifies data comparison. The data shared on this site has been uploaded with permission from the institution that generated it. The data is converted in a standard format at upload, and typical statistical quantities are calculated if they were missing from the original dataset. We encourage the following code of conduct for the use of the data and site.

1. Use of any data featured on this site for publication purposes should include references to the article that describes the experiments conducted for generating the data.
2. Individual groups may have additional guidelines for the use of their data. In such cases, we link to the group’s website for these policies.
3. Please cite www.batteryarchive.org as the source from where the data was downloaded.
4. Send us a reference to work that uses the data, and we will add it to our publication list.

More details about the list of studies can be found online:

https://batteryarchive.org/study_summaries.html



For questions, email info@batteryarchive.org.
