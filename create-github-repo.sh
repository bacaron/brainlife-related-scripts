#!/bin/bash

startDir=pwd
repopath=$1
reponame=$2
username=$3

[ ! -d $repopath ] && mkdir - p $repopath && cd $repopath

# git related functions
git init # initialize the directory as a github repo
cat "# $reponame" >> README.md # generate blank README
git add . # add files
git commit -m "reason: initial commit" # message describing updates
curl -u $username https://api.github.com/user/repos -d '{"name":$reponame,"private":false}' # creates new repo
git remote add origin https://github.com/$username/$reponame # adds remote repository as origin
git branch -m master main # changes name of top branch from master to main
git push -u origin main # pushes changes to main branch

cd $startDir
