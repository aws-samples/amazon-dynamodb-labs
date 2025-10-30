import os
import re
import sys
import time
import glob
import shutil
import ntpath
import tempfile
import subprocess
from pathlib import Path
from zipfile import ZipFile


pkg_root = os.getenv("GITHUB_WORKSPACE")
if not pkg_root:
    pkg_root = os.getcwd()

dest_root = os.path.join(pkg_root, 'public')



#clear out the assets folder
shutil.rmtree(os.path.join(dest_root,'assets'), ignore_errors=True)

#Move static assets
Path(dest_root, 'assets').mkdir(parents=True, exist_ok=False)
data_files = ['design-patterns/cloudformation/vscode.yaml',
    'design-patterns/cloudformation/UserDataC9.sh',
    'event-driven/event-driven-cfn.yaml',
    'static/files/hands-on-labs/migration-env-setup.yaml',
    'static/files/hands-on-labs/migration-dms-setup.yaml',
    'static/files/dynamodb-opensearch-zetl/dynamodb-opensearch-setup.yaml'
]
for inp_file in data_files:
    src_file = os.path.join(pkg_root, inp_file)
    head, tail = ntpath.split(src_file)
    dst_file =  os.path.join(dest_root, 'assets', tail or ntpath.basename(head))
    shutil.copyfile(src_file, dst_file)

#Create workshop ZIP
os.chdir(os.path.join(pkg_root, 'design-patterns'))
with ZipFile('workshop.zip', 'w') as workshop_zip:
	for py_script in glob.glob('./*.py'):
		workshop_zip.write(py_script)
	for txt_script in glob.glob('./*.txt'):
		workshop_zip.write(txt_script)
	for js_script in glob.glob('./*.json'):
		workshop_zip.write(js_script)
	for data_file in glob.glob('./data/*.csv'):
		workshop_zip.write(data_file)
shutil.move(os.path.join(os.getcwd(), 'workshop.zip'), os.path.join(dest_root, 'assets', 'workshop.zip'))


#Create solution ZIP
os.chdir(os.path.join(pkg_root, 'scenario-solutions'))
with ZipFile('scenario-solutions.zip', 'w') as workshop_zip:
	for scenario1 in glob.glob('./retail-cart/*'):
		workshop_zip.write(scenario1)
	for scenario2 in glob.glob('./bank-payments/*'):
		workshop_zip.write(scenario2)
shutil.move(os.path.join(os.getcwd(), 'scenario-solutions.zip'), os.path.join(dest_root, 'assets', 'scenario-solutions.zip'))

#Create LHOL zETL ZIP
os.chdir(os.path.join(pkg_root, 'static', 'files', 'dynamodb-opensearch-zetl'))
with ZipFile('OpenSearchPipeline.zip', 'w') as workshop_zip:
	for pyscript in glob.glob('./OpenSearchPipeline/*'):
		workshop_zip.write(pyscript)
shutil.move(os.path.join(os.getcwd(), 'OpenSearchPipeline.zip'), os.path.join(dest_root, 'assets', 'OpenSearchPipeline.zip'))


#Create Game-Player-Data Python Scripts ZIP
os.chdir(os.path.join(pkg_root, 'game-player-data'))
with ZipFile('battle-royale.zip', 'w') as workshop_zip:
	for pyscript in glob.glob('./scripts/*.py'):
		workshop_zip.write(pyscript)
	for js_script in glob.glob('./scripts/*.json'):
		workshop_zip.write(js_script)
shutil.move(os.path.join(os.getcwd(), 'battle-royale.zip'), os.path.join(dest_root, 'assets', 'battle-royale.zip'))

#Create Global Serverless ZIP
os.chdir(os.path.join(pkg_root, 'global-serverless'))
with ZipFile('global-serverless.zip', 'w') as workshop_zip:
	for data_file in glob.glob('global-serverless/*'):
		workshop_zip.write(data_file)
	workshop_zip.write('global-serverless/.chalice/config.json')
shutil.move(os.path.join(os.getcwd(), 'global-serverless.zip'), os.path.join(dest_root, 'assets', 'global-serverless.zip'))


#Create Event Driven ZIPs
zips_to_make = ['MapLambdaPackage', 'ReduceLambdaPackage', 'StateLambdaPackage', 'GeneratorLambdaPackage']
for zip_name in zips_to_make:
    os.chdir(os.path.join(pkg_root, 'event-driven', zip_name))
    zip_file_name = "{}.zip".format(zip_name)
    with ZipFile(zip_file_name, 'w') as workshop_zip:
        for python_script in glob.glob("./*.py".format(zip_name)):
            head, tail = ntpath.split(python_script)
            workshop_zip.write(python_script, tail)
    shutil.move(os.path.join(os.getcwd(), zip_file_name), os.path.join(dest_root, 'assets', zip_file_name))

# Check build

preview_build = os.path.join(pkg_root, 'preview_build')
shell_out = tempfile.NamedTemporaryFile(mode='w')
try:
    proc = subprocess.Popen([preview_build,"-disable-refresh"],
		stdout=shell_out, stderr=shell_out, cwd=pkg_root)
except FileNotFoundError as err:
	proc = subprocess.Popen(["preview_build", "-disable-refresh"],
		stdout=shell_out, stderr=shell_out, cwd=pkg_root)


time.sleep(10)
proc.kill()
build_result_error = r'.*(Build complete with [0-9].*)'
build_result_success = r'.*(Build succeeded.*)'
status = None
status_message = None
count = 0
with open(shell_out.name) as f:
    for line in f:
        if count > 10000:
            break
        count += 1
        if status == None:
            match_error = re.search(build_result_error, line)
            match_success = re.search(build_result_success, line)
            if match_error:
                status_message = match_error.group(1)
                status = 1
                print("Discovered an error in the build process.\n{}".format(status_message))
            elif match_success:
                status_message = match_success.group(1)
                status = 0
                print("Success. Build result is: \n{}".format(status_message))
        elif status == 1:
            err_match = re.search(r'^.*ERR(.*)', line)
            err_ignore = re.search(r'^.*Error hosting local preview site.*', line)
            if err_match and err_ignore is None:
                print("{}".format(err_match.group(1)))

shell_out.close()
exit(status)
