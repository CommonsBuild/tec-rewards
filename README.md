**[NOTE: This is a Work-In-Progress. The default settings take inputs stored in "test_inputs" and save them in a folder called "round_x", using dummy notebooks]**
# Modular R.A.D Dashboard

This is the repository for the modular Reward Analysis and Distribution Dashboard (R.A.D.D). The system takes a set of raw  DAO activity records and calculates a corresponding token distribution, along with generating HTML reports analyzing the data. This is done through a set of interconnected Jupyter notebooks.

This program is intended to run on the backend server of a DAO's reward system, and will automatically push the results to a github repository for easy auditability by non-technical DAO members.

## Setup
 
0.  As a beginning step, it is recommended to create a fresh python virtual environment for the installation. A tutorial using ``virtualenv`` can be found [here](https://www.tutorialspoint.com/python-virtual-environment) or you can use [anacoda to manage environments](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands). 

  You will need **python 3.9**. For example, using conda, you type in ``conda create -n rad_venv python=3.9`` then use ``conda activate rad_venv`` to run it.

1. Once we are inside the virtual environment, run tho following command in the root folder:   

```bash
pip install -r requirements.txt
```
2. Now you just have to run 
```bash 
 python rad_main.py -p parameters.json
```

The script will take the information in the specified parameters file and save the resulting artefacts in a new folder inside the "distribution_results" folder. This folder is intended to be easily auditable and in a production system would probably be a separate repository for clear access control.

The running of the script is intended to be automatable. In an ideal case it would be just appended to the regular "reward period closing" in the backend, and generate all outputs without human intervention.

## Workstream
The script will take a set of csv files and apply a group of reward systems systems to them as specifed in the JSON parameters file. 
- First, it will calculate the distribution of reward tokens and export it  by running the data through a "distribution notebook", where the reards algorithm lives.
- The resulting data is then fed to a set of separate analysis notebooks templates, each designed to grant insights into a specific aspect of the distribution. These notebooks use analysis methods stored in the form of python modules to generate HTML report files, which can then easily be accessed (while keeping graphs interactive, as opposed to PDF files).  

At the end of the process, following files will have been stored, ready to be pushed to github:
- A copy of all the raw data used to generate the distribution
- CSV files containing the resulting distribution, both in human-readable and machine-feedablr formats (WIP in the current version)
- One HTML report for each analysis.
- Backup copies of all the run notebooks in their finalized state, with the data used in that round. These contain exactly the same information as the HTML reports, but add the code cells that generated it. They are stored exclusively to facilitate future audits. 

## How will different types of users interact with the system?

### Non-technical DAO members
This is expected to be the majority of the users. They can access the results repository and freely download and run the reports in their browser without needing to install anything. They can also import the csv files to excel or google docs. The result notebooks can be audited online with mybinder.

### System administrator
Administrators are expected to install this system on the backend server and generate compatible input JSON files.  In the JSON file they can specify which praise systems to use, how many tokens to distribute to each systems, and more system-specific settings. Afterwards they can manually store the resulting folder on Github.

### Other developers 
If other DAOs want to integrate the dashboard and add their own reward systems, this can be done easily. They only need to create a new set of notebooks and save them in a correctly labeled folder. Since most of the logic is saved in the external python modules, they can easily import already developed analytics into their own framework. They can also copy the existing notebooks modify them to suit their needs. Since Jupyter supports several programming languages, they can even develop the notebooks in the language of their choice and have them integrate with the rest of the system out of the box. 

## Future developments
-Automatic Github export (high priority)
-Integration with backend database (so csv exports aren't necessary)
-POSSIBLY: Hosted frontend on which to access distribution results and load the HTMLs in a more user-friendly way, in the style of [this image](https://images.zenhubusercontent.com/5fdba670baa205320c5a291e/0e7b21b2-a8ec-40e4-9a31-07f6d64eb4bb)
