# Access-Point-Simulator-and-Analysis-Program
This program will contain the different version of an access point simulation program. 

## Version 1
This first version would only contain the mechanics of opening a building blueprint and adding access point objects. 

### How will I add the building blueprint?
There will be a function that'll add an image for a building blueprint. This image viewing mechanics would need the blueprint to be shown in full. As such, there should also be a highly customizable zoom and moving function.

### How will I add the access points?
There must be a button on the gui which is labeled as add_accessPoint. Once clicking this button, the user should be able to click anywhere on the blueprint and a node is added.

## Version 2
This second version would add circles denoting wifi/signal heats. These circles would be colored from red to yellow to green depending on the strength of the signal and number of connection points.

### How will I add the signal heat zones?
There must be a button on the gui which is labeled as "add signal heat zone". Once clicking this button, the user should be able to click anywhere on the blueprint and a heat zone is added. Then, a dialog would be opened where the characteristics of the heatzone is specified.


### How will I set the coverage sizes, number of connection points and their respective signal strength of each of the wifi/signal heat zone?
After clicking the add signal heat zone button then clicking on the blueprint, in the dialog there would be prompts asking the coverage size, and the connection point then its respective signal strength. There might be multiple connection points, as such there should be an add connection point button in this dialog.

### How will the visual illustration of the signal strength within the heat zone be determined?
The determination process will be dependent on the number of connection points and their respective signal strength. From this, create a calculation.

