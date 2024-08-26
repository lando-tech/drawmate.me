# diagram_me
 Automate wiremaps and diagrams using draw.io format.

 !!! This program is still under development !!! Looking for active contributers. Make a fork if interested.

 IT professionals utilize draw.io regularly to create wiremaps and diagrams to show logical connections of various network appliances
 with a multitude of architectures. This program aims to automate this process by 4 main approaches:
 1. Generate a csv/database structure of appliances and products by scrapping the text out of PDF files imported into the program. This allows for a base of knowledge for the program to pull from.
 2. Update connections: The program will use an API structure to update connection rules based on user input, i.e if the user wants all n number of workstations to connect to n number of switches.
 3. Convert existing diagrams: In xml2json, this script converts an existing draw.io XML file to JSON. This JSON file is then saved and stored as a 'template' for later use. This program will also update connection rules based on the provided XML file.
 4. Once the file has been converted and the template saved, the user simply chooses from a templates that has been created, and the json2xml will then convert the JSON template into draw.io XML format.

Current Issues:
I am currently working through the process of converting back to draw.io XML format and also updating the JSON to refelct both connection preferences and template changes. 
It currently converts the JSON back to XML format, but draw.io does not always recognize the embeded javascript inside the file. 

 
