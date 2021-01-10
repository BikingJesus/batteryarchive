#File name: data_transfer.py allow downloading data from www.batteryarchive.org
#Copyright (C) 2021 Valerio De Angelis

#Utility to download files from wwww.batteryarchive.org.
#given a metadata files in csv format, generate the links and download cycle data and time series data
#cycle data file format: http://www.batteryarchive.org/data/[data_set]/[cell_id]_cycle_data.csv
#time data file format http://www.batteryarchive.org/data/[data_set]/[cell_id]_timeseries.csv
#files are donwload to the folder that contains the csv and python file
#For questions, email info@batteryarchive.org

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.

#data_transfer.py Copyright (C) 2021  Valerio De Angelis
#This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#This is free software, and you are welcome to redistribute it
#under certain conditions; type `show c' for details.


import pandas as pd
import requests
import sys


def get_file(path, save_to_file_name):
    print(path)
    req = requests.get(path)
    url_content = req.content
    csv_file = open(save_to_file_name, 'wb')

    csv_file.write(url_content)
    csv_file.close()


data_set = 'metadata'
prefix = "https://www.batteryarchive.org/data/"
try:
    df_snl = pd.read_csv("./" + data_set + ".csv")
    print(df_snl)

    number_of_cells = str(len(df_snl))

    for ind in df_snl.index:
        cell_id = df_snl['cell_id'][ind]
        file_name = cell_id.replace("/", "-")

        print(str(ind+1) + " of " + number_of_cells + ": Cycle data cell_id: " + cell_id)
        cycle_data = prefix + file_name + "_cycle_data.csv"
        get_file(cycle_data, file_name + "_cycle_data.csv")

        print(str(ind+1) + " of " + number_of_cells + ": Time data cell_id: " + cell_id)
        time_data = prefix + file_name + "_timeseries.csv"
        get_file(time_data, file_name + "_timeseries.csv")

    print("Done downloading files. Thank you for using www.batteryarchive.org")
    print("For questions on how to add your data, contact info@batteryarchive.org")


except OSError as e:
    print("Error reading data_set: " + str(e))
    print("please send the complete message to info@batteryarchive.org")

except:
    print("Unexpected error: ", sys.exc_info()[0])
    print("please send the complete message to info@batteryarchive.org")