# Backend Setup:

Setting up the backend for the web-app involves generating a database from the revit project you wish to visualise. In order to do this you will first need to install some dependencies.

## Dependencies:
### Autodesk Revit:

You will need to have some version of Revit installed, which you are able to open your project with. This system is dependent on Revit so if you don’t have access to Revit you will not be able to use this portion of the project.

### pyRevit:

To run the script that generates the database you will need to have the Revit extension PyRevit installed, which can be found at this link: https://github.com/eirannejad/pyRevit/releases. Make sure you have Revit installed before trying to install PyRevit, or the installation will not work. Following the default setup instructions for PyRevit will be fine for this product.

## Setting up a pyRevit Button:
First of all, check that pyRevit has been installed correctly. This can be done by closing Revit if it is already open, and reopening it, opening a project, and looking at the panels along the top of the project. If there is an additional tab to the right of “Add-ins” called pyRevit then pyRevit has installed correctly.

Now navigate to the folder where pyRevit extensions are located, by default on windows this is C:\Users\USERNAME\AppData\Roaming\pyRevit-Master\extensions, where USERNAME is the folder for the account currently logged into the computer. If you have trouble finding this you can easily navigate to C:\Users\USERNAME\AppData\Roaming\ by typing “%appdata%” into the windows search bar and pressing enter. If you are unable to find pyRevit-Master in this location then either pyRevit isn’t installed, or has been installed somewhere else, which you may have specified during pyRevit’s installation.

Once you are in the extensions folder you will need to create a series of nested folders so that pyRevit recognises the extension properly. First create a folder named “loadToDB.extension”, then enter this folder, and create another folder called “loadToDB.tab” and open this folder, then create another folder called “loadToDB.panel” and open this folder, then make another folder called “runScripts.pushbutton”.

Now you need to put the scripts from the project folder into the button, so pyRevit knows what code to run when the button is pressed. Copy the files “DocumentInterface.py”, “sqliteRevitIpy.py” and “RevitLoader_script.py” from the src folder in the project, to the “runScripts.pushbutton” folder. 

Open DocumentInterface.py in a text editor (e.g. notepad) and remove the # and space at the start of the first line, then close and save the file.

Close Revit, then open it again, and open a project. There should now be a new panel on the tabs at the top of the project, next to pyRevit, called loadToDB. Clicking on this panel should open up a tab with a button labelled runScripts on it. If this works then you are ready to move on to the next step.

## Generating and Using the database:
To generate your database simply click the runScripts button. This will open up a terminal that will run through the scripts to make your database. It will spit out a lot of information to show that it is working, but this is not important to you.

Once the script is done running there should be a file called db.sqlite in the folder with the scripts. Copy and paste this into the XYZ folder. You are now done with backend setup.


