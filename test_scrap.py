import papermill as pm
import scrapbook as sb
import oyaml as yaml
import subprocess
 
# Opening JSON file
parsed_yaml = []
with open("./parameters.yaml", 'r') as stream:
    try:
        parsed_yaml=yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

pm.execute_notebook(
   './praiseDist_test.ipynb',
   './output_distTest.ipynb',
   parameters = parsed_yaml
)

pm.execute_notebook(
   './praiseAnalysis_test.ipynb',
   './output_AnalysisTest.ipynb',
)

#after that, running the following command in the terminal will output a pretty HTML with all the graphs but none of the code.
return_buf = subprocess.run("jupyter nbconvert --to html --TemplateExporter.exclude_input=True output_AnalysisTest.ipynb", shell=True)


