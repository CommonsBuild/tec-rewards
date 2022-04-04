import papermill as pm
import scrapbook as sb
import oyaml as yaml
import subprocess
import sys, json, os
from pathlib import Path
import math
 

params = {}
with open("parameters.json", "r") as read_file:
    params = json.load(read_file)

OUTPUT_PATH = "./" + params["results_output_folder"] + "/" + params["distribution_name"] + "/"

#create output file structure:
Path(OUTPUT_PATH).mkdir(parents=True, exist_ok=True)
Path(OUTPUT_PATH + "results/").mkdir(parents=True, exist_ok=True)
Path(OUTPUT_PATH + "results/output_notebooks/").mkdir(parents=True, exist_ok=True)
Path(OUTPUT_PATH + "results/reports/").mkdir(parents=True, exist_ok=True)
Path(OUTPUT_PATH + "results/distribution/").mkdir(parents=True, exist_ok=True)

#TO DO copy all input data into the main results folder


#apply all specified reward systems
for i, reward_system in enumerate(params["employed_reward_systems"]):
	#TO DO: MOVE THIS TO INDEPENDENT FUNCTIONS FOR EACH SYSTEM AND CREATE __INIT__ !!!!
	if reward_system == "praise":
		total_tokens_allocated = params["token_allocation_per_reward_system"][i]
		system_params = params["system_settings"][reward_system]
		
		#we add the results path for the exports
		system_params["distribution_name"] = params["distribution_name"]
		system_params["results_output_folder"] = params["results_output_folder"]
	 
		
		print(system_params["token_reward_percentages"]["contributor_rewards"])
		
		#distribution
		dist_input_path = "./distribution_tools/" + reward_system + "/praiseDist_test.ipynb"
		dist_output_path = OUTPUT_PATH + "results/output_notebooks/output_distTest.ipynb"
		
		print(dist_output_path)

		pm.execute_notebook(
		   dist_input_path,
		   dist_output_path,
		   parameters = system_params
		)
		
		#analysis

		#for each notebook
		ANALYSIS_ROOT_PATH= "./analysis_tools/notebooks/praise/"
		analysis_params= {"dist_notebook_path": dist_output_path}
		for notebook in os.listdir(ANALYSIS_ROOT_PATH):
			#TO DO make sure its a .ipynb file (save name while we are at it)
			
			#run it
			INPUT_NOTEBOOK_PATH = ANALYSIS_ROOT_PATH + notebook
			OUTPUT_NOTEBOOK_PATH = ANALYSIS_ROOT_PATH + "output_" + notebook
			pm.execute_notebook(
				INPUT_NOTEBOOK_PATH,
   				OUTPUT_NOTEBOOK_PATH,
   				parameters = analysis_params
			)
			# generate HTML report
			return_buf = subprocess.run("jupyter nbconvert --to html --TemplateExporter.exclude_input=True %s"%OUTPUT_NOTEBOOK_PATH, shell=True)
			#move it to right folder
			
			
			#TO DO: sort out moving the result notebook and the HTML
			
			#NEW_OUTPUT_PATH = OUTPUT_PATH + "results/output_notebooks/output_" + notebook
			#os.rename(OUTPUT_NOTEBOOK_PATH, NEW_OUTPUT_PATH)

			
	if reward_system == "sourcecred":
		print("Sourcecred not implemented")




#import params.json
#save basic data (output path ) 
#for each [reward_system]
	#send data to distribution notebook
	#save results to output path
	#perform analysis
	#save results to output path
	#for each [analysis notebook result]
		#export that notebook to html
