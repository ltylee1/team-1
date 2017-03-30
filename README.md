<img src="https://raw.githubusercontent.com/UBC-CPSC319/team-1/master/uw_dashboard/static/images/dashboard.jpeg" alt="Drawing" style="width: 100px;"/>
## United Way Program and Agency Database

###Instalation Instructions 

####Prerequesits
The system was tested using Ubuntu 16.04.2 LTS but any popular distribution of linux can be used. 

**Step 1. Preparing the virtual environment**

The best way to run the application is within a contained virtual environment using `virtualenvwrapper`. Make sure you have `python-pip` (ubuntu apt-get) and `python` installed. the recommended version of python for this project is 2.7.


First, install virtualenvwrapper using the following command:
`$ pip install virtualenvwrapper`

Then edit your .bashrc by adding the following lines on to the end of the file located in your home folder. Its usually `~/.bashrc`

```
export WORKON_HOME=~/Envs
mkdir -p $WORKON_HOME
source /usr/local/bin/virtualenvwrapper.sh
```
Restart the virtual machine (or close the terminal and open it again) and then run `$ mkvirtualenv unitedway`

Note:

Whenever you are running the application make sure to run the command `$ workon unitedway` first.

**Step 2. Cloning and installing dependencies**

First, make sure that you are in the virtual environment that you created in step 1 by running the command `$ workon unitedway`


Make sure that `git` is installed and clone the github project to any folder by running the command:

`$ git clone git@github.com:UBC-CPSC319/team-1.git`

go in to the folder that was just created and install the required `pip` packages by running the following commands:

```
$ cd team-1
$ pip install -r requirments.txt
```
 
 
