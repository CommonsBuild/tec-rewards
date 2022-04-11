import os
import subprocess
import json
import shutil
from pathlib import Path

import papermill as pm
import scrapbook as sb

import argparse


parser = argparse.ArgumentParser(
    description='RAD main script')
parser.add_argument("-p", "--parameters", type=str, required=True,
                    help="File with the distribution parameters")

args = parser.parse_args()
input_parameters = args.parameters


params = {}
with open(input_parameters, "r") as read_file:
    params = json.load(read_file)

# declare the paths where we want to save stuff as constants for easy reference
ROOT_OUTPUT_PATH = "./" + \
    params["results_output_folder"] + "/" + params["distribution_name"] + "/"
RAW_DATA_OUTPUT_PATH = ROOT_OUTPUT_PATH + "data/"
NOTEBOOK_OUTPUT_PATH = ROOT_OUTPUT_PATH + "results/analysis_outputs/"
REPORT_OUTPUT_PATH = ROOT_OUTPUT_PATH + "results/reports/"
DISTRIBUTION_OUTPUT_PATH = ROOT_OUTPUT_PATH + "results/distribution/"

# create output file structure:
Path(ROOT_OUTPUT_PATH).mkdir(parents=True, exist_ok=True)
Path(RAW_DATA_OUTPUT_PATH).mkdir(parents=True, exist_ok=True)
Path(NOTEBOOK_OUTPUT_PATH).mkdir(parents=True, exist_ok=True)
Path(REPORT_OUTPUT_PATH).mkdir(parents=True, exist_ok=True)
Path(DISTRIBUTION_OUTPUT_PATH).mkdir(parents=True, exist_ok=True)

# save all input files into the /results/data folder
for system_name in params["employed_reward_systems"]:
    for system_data in params["system_settings"]:
        if system_name == system_data:
            for in_file in params["system_settings"][system_data]["input_files"]:
                input_path = params["system_settings"][system_data]["input_files"][in_file]
                # print(input_path)
                shutil.copy(input_path, RAW_DATA_OUTPUT_PATH)
# Also save the distribution params
shutil.copy(input_parameters, RAW_DATA_OUTPUT_PATH)

# apply all specified reward systems
for i, reward_system in enumerate(params["employed_reward_systems"]):

    # ====== DISTRIBUTION =========

    # prepare the parameter set we will send to the distribution and the folder with the notebook templates
    system_params = params["system_settings"][reward_system]
    system_params["total_tokens_allocated"] = params["token_allocation_per_reward_system"][i]
    system_params["distribution_name"] = params["distribution_name"]
    system_params["results_output_folder"] = params["results_output_folder"]

    DISTRIBUTION_NOTEBOOK_FOLDER = "./distribution_tools/" + reward_system + "/"

    # run all notebooks in the relevant distribution folder
    for notebook in os.listdir(DISTRIBUTION_NOTEBOOK_FOLDER):
        # make sure we only use .ipynb files
        if not (notebook.endswith(".ipynb")):
            continue

        dist_input_path = DISTRIBUTION_NOTEBOOK_FOLDER + notebook
        dist_output_path = NOTEBOOK_OUTPUT_PATH + "output_" + notebook

        # print(dist_output_path)

        pm.execute_notebook(
            dist_input_path,
            dist_output_path,
            parameters=system_params
        )

    # copy generated distribution files to results folder
    for output_csv in os.listdir():
        if not (output_csv.endswith(".csv")):
            continue
        #print(output_csv)
        csv_destination = DISTRIBUTION_OUTPUT_PATH + output_csv
        os.rename(output_csv, csv_destination)

    # ====== ANALYSIS =========

    # prepare the parameter set we will use for analysis and the folder with the notebook templates
    analysis_params = {"dist_notebook_path": dist_output_path}

    ANALYSIS_NOTEBOOK_FOLDER = "./analysis_tools/notebooks/" + reward_system + "/"

    # run all notebooks in the analysis folder
    for notebook in os.listdir(ANALYSIS_NOTEBOOK_FOLDER):

        # make sure we only use .ipynb files
        if not (notebook.endswith(".ipynb")):
            continue

        nb_input_path = ANALYSIS_NOTEBOOK_FOLDER + notebook
        nb_destination_path = NOTEBOOK_OUTPUT_PATH + "output_" + notebook

        pm.execute_notebook(
            nb_input_path,
            nb_destination_path,
            parameters=analysis_params
        )

        # generate HTML report
        return_buf = subprocess.run(
            "jupyter nbconvert --to html --TemplateExporter.exclude_input=True %s" % nb_destination_path, shell=True)

        # move any generated analysis csv files to the right folder
        for analysis_csv in os.listdir(ANALYSIS_NOTEBOOK_FOLDER):
            if not (analysis_csv.endswith(".csv")):
                continue

            #print(analysis_csv)
            csv_destination = NOTEBOOK_OUTPUT_PATH + analysis_csv
            #print(csv_destination)
            os.rename(analysis_csv, csv_destination)

        # move it to right folder
        html_report_origin = nb_destination_path[:-6] + ".html"
        html_report_destination = REPORT_OUTPUT_PATH + \
            notebook[:-6] + "_Report.html"
        os.rename(html_report_origin, html_report_destination)
