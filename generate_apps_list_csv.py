#!/usr/bin/env python3

import json
import subprocess
import pandas as pd
import numpy as np
import sys, argparse

def identify_my_apps(contributor_name):

	output = subprocess.Popen("singularity exec -e docker://brainlife/cli:latest bl app query -l 1000000 -j", shell=True, stdout=subprocess.PIPE, encoding="utf-8")
	outs,errs  = output.communicate()
	apps = json.loads(outs)
	my_apps = np.array([],dtype=object)

	for num_apps in range(len(apps)):
			for contributors in apps[num_apps]['contributors']:
				if contributors['name'] == contributor_name:
					my_apps = np.append(my_apps,apps[num_apps])

	return my_apps

def generate_apps_list_csv(contributor_name,savedir,savename):

	df = pd.DataFrame(columns=["Name","Github_repo","Github_branch","DOI","Brainlife_link"],dtype=object)

	my_apps = identify_my_apps(contributor_name)
	df["Name"] = [str(my_apps[name]["name"]) for name in range(len(my_apps))]
	df["Github_repo"] = [my_apps[repo]["github"] for repo in range(len(my_apps))]
	df["Github_branch"] = [my_apps[branch]["github_branch"] if 'github_branch' in my_apps[branch] else 'none' for branch in range(len(my_apps))]
	df["DOI"] = [my_apps[doi]["doi"] for doi in range(len(my_apps))]
	df["Brainlife_link"] = ['https://brainlife.io/app/%s' %str(my_apps[id]["_id"]) for id in range(len(my_apps))]

	df.to_csv('%s/%s.csv' %(savedir,savename),index=False)


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Creating csv of your brainlife apps')
	parser.add_argument("--contributor_name", default=None, type=str, help="Your name to use to indentify your apps")
	parser.add_argument("--savedir", default=None, type=str, help="Save directory path for the output csv")
	parser.add_argument("--savename", default=None, type=str, help="File name for the output csv")


	args = parser.parse_args()
	generate_apps_list_csv(args.contributor_name,args.savedir,args.savename)
