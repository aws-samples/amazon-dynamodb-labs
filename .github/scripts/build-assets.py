import os
import sys
import glob
import shutil
import ntpath
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
data_files = ['design-patterns/cloudformation/lab.yaml',
    'design-patterns/cloudformation/C9.yaml',
    'design-patterns/cloudformation/UserData.sh',
    'design-patterns/cloudformation/UserDataC9.sh',
    'event-driven/event-driven-cfn.yaml',
    'static/files/hands-on-labs/migration-env-setup.yaml',
    'static/files/hands-on-labs/migration-dms-setup.yaml']
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

exit()
