#!/bin/bash

startDir=$(eval pwd)
repopath=$1
reponame=$2
username=$3

# make new repo directory
[ ! -d $repopath ] && mkdir -p $repopath && cd $repopath

# grab github public access key
pubkey=`cat ~/.ssh/gitkeys`

# git related functions
git init # initialize the directory as a github repo
echo "# $reponame" >> README.md # generate blank README
git add . # add files
git commit -m "reason: initial commit" # message describing updates
dict=`echo $(printf '{"name":"%q","private":false}' "$reponame")` # set up json dictionary to pass into curl command
curl -u $username:$pubkey https://api.github.com/user/repos -d $dict # creates new repo
eval git remote add origin https://github.com/$username/$reponame # adds remote repository as origin
eval git remote set-url origin git@github.com:$username/$reponame.git # set url origin
git branch -m master main # changes name of top branch from master to main
git push -u origin main # pushes changes to main branch

cd $startDir
