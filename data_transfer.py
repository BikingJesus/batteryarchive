# File name: data_transfer.py allow downloading data from www.batteryarchive.org
# Copyright (C) 2021 Valerio De Angelis

# Utility to download files from wwww.batteryarchive.org.
# given a metadata files in csv format, generate the links and download cycle data and time series data
# cycle data file format: http://www.batteryarchive.org/data/[data_set]/[cell_id]_cycle_data.csv
# time data file format http://www.batteryarchive.org/data/[data_set]/[cell_id]_timeseries.csv
# files are donwload to the folder that contains the csv and python file
# For questions, email info@batteryarchive.org

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# data_transfer.py Copyright (C) 2021  Valerio De Angelis
# This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
# This is free software, and you are welcome to redistribute it
# under certain conditions; type `show c' for details.

import argparse
import sys
from pathlib import Path
import pandas as pd
import requests
import numpy as np
from tqdm import tqdm

metadata_file = Path('metadata.csv')
metadata = pd.read_csv(metadata_file, index_col=0)


def get_file(path, save_to_file_name):
    save_to_file_name.parent.mkdir(exist_ok=True, parents=True)
    req = requests.get(path)
    url_content = req.content
    csv_file = open(save_to_file_name, 'wb')

    csv_file.write(url_content)
    csv_file.close()


def add_soh_snl(cell_id, file):
    capacity = metadata['capacity_ah'][cell_id]

    df = pd.read_csv(file, index_col=0)

    # see e.g. SNL_18650_NMC_25C_20-80_0.5-3C_a_cycle_data.csv
    df.drop_duplicates(subset=df.columns, inplace=True)
    df['SoH (%)'] = np.nan

    # Capacity measurements seem to be indicated by an empty cycle
    pre_measurement_condition = (df['Charge_Capacity (Ah)'] == 0) & (df['Discharge_Capacity (Ah)'] == 0) & (
            df['Min_Voltage (V)'] > 0) & (df['Max_Voltage (V)'] > 0) & (
                                        df['Min_Current (A)'] == 0) & (df['Max_Current (A)'] == 0)
    measurements = [i for i, cond in enumerate(pre_measurement_condition) if cond]

    # Starting point
    measurements += [-1]

    for i in measurements:
        # The capacity is measured in the cycles around that empty cycle.
        for j in range(max(0, i - 2), min(i + 4, len(df))):
            if j in measurements:
                continue
            df.at[df.index[j], 'SoH (%)'] = df['Discharge_Capacity (Ah)'][df.index[j]] / capacity * 100

    df.to_csv(file)


def add_soh(cell_id, file):
    if not file.exists():
        print(
            f'File "{file}" not found. Cannot add SoH. If not yet downloaded use the --cycle-data flag',
            file=sys.stderr)
        return

    if metadata['study'][cell_id].lower() == 'snl':
        add_soh_snl(cell_id, file)
        return

    capacity = metadata['capacity_ah'][cell_id]
    df = pd.read_csv(file, index_col=0)
    df.sort_values(by='Cycle_Index', inplace=True)
    df['SoH (%)'] = df['Discharge_Capacity (Ah)'] / capacity * 100
    df.to_csv(file)


def add_efc(cell_id, file):
    if not file.exists():
        print(
            f'File "{file}" not found. Cannot add equivalent full cycle column.'
            f' If not yet downloaded use the --cycle-data flag',
            file=sys.stderr)
        return
    min_soc = metadata['min_soc'][cell_id]
    max_soc = metadata['max_soc'][cell_id]

    dod = max_soc - min_soc

    df = pd.read_csv(file)
    df['Equivalent Full Cycles'] = df['Cycle_Index'] * dod / 100
    df.to_csv(file, index=False)


def add_metadata(cell_id, file, metadata_keys):
    if not metadata_keys:
        return

    df = pd.read_csv(file)
    for m in metadata_keys:
        if m not in metadata.columns:
            print(f'{m} is not a proper column name in "{metadata_file}". Available are: {", ".join(metadata.columns)}',
                  file=sys.stderr)
            exit(1)
        df[m] = metadata[m][cell_id]

    df.to_csv(file, index=False)


def get_all(cycle_data, time_series, destination, soh, efc, dir_by_meta, metadata_keys):
    prefix = "https://www.batteryarchive.org/data/"
    destination = Path(destination)
    try:
        print(metadata)
        for cell_id in tqdm(metadata.index):
            file_name = cell_id.replace("/", "-")
            folder = destination

            for meta_dir in dir_by_meta:
                if meta_dir not in metadata.columns:
                    print(
                        f'{meta_dir} is not a proper column name in "{metadata_file}". Available are: {", ".join(metadata.columns)}',
                        file=sys.stderr)
                    exit(1)
                folder /= metadata[meta_dir][cell_id]

            cycle_data_file = folder / f'{file_name}_cycle_data.csv'
            time_series_file = folder / f'{file_name}_timeseries.csv'

            if cycle_data:
                cycle_data = prefix + file_name + "_cycle_data.csv"
                get_file(cycle_data, cycle_data_file)
                add_metadata(cell_id, cycle_data_file, metadata_keys)

            if time_series:
                time_data = prefix + file_name + "_timeseries.csv"
                get_file(time_data, time_series_file)
                add_metadata(cell_id, time_series_file, metadata_keys)

            if soh:
                add_soh(cell_id, cycle_data_file)

            if efc:
                add_efc(cell_id, cycle_data_file)

        print("Done downloading files. Thank you for using www.batteryarchive.org")
        print("For questions on how to add your data, contact info@batteryarchive.org")


    except OSError as e:
        print("Error reading data_set: ")
        print("please send the complete message to info@batteryarchive.org")
        raise

    except Exception as e:
        print("Unexpected error: ")
        print("please send the complete message to info@batteryarchive.org")
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Downloads data from www.batteryarchive.org.')
    parser.add_argument('--dest', '-d', type=str, dest='dest', default='.',
                        help='Folder in which the data shall be placed. (Default cwd)')
    parser.add_argument('--cycle-data', '-c', dest='cycle', action='store_true',
                        help='If set, the cycle data will be downloaded')
    parser.add_argument('--time-series', '-t', dest='time', action='store_true',
                        help='If set, the time series will be downloaded')
    parser.add_argument('--soh', dest='soh', action='store_true',
                        help='If set, soh will be calculated')
    parser.add_argument('--efc', dest='efc', action='store_true',
                        help='If set, equivalent full cycles will be added')
    parser.add_argument('--dir-by-meta-data', dest='dir_by_meta', nargs='+', type=str, default=list(),
                        help='You can specify several metadata columns.'
                             ' The corresponding values will be used as folders.')
    parser.add_argument('--meta-data', dest='metadata', nargs='+', type=str, default=list(),
                        help='You can specify metadata to be added as columns to the data.')

    args = parser.parse_args()

    get_all(
        cycle_data=args.cycle,
        time_series=args.time,
        destination=args.dest,
        soh=args.soh,
        efc=args.efc,
        dir_by_meta=args.dir_by_meta,
        metadata_keys=args.metadata)
