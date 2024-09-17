# drawmate.me
 Automate wiremaps and diagrams using draw.io format.

 !!! This program is still under development !!! Looking for active contributers. Make a fork if interested.

 IT professionals utilize draw.io regularly to create wiremaps and diagrams to show logical connections of various network appliances
 with a multitude of architectures. This program aims to automate this process by 4 main approaches:
 1. Generate a csv/database structure of appliances and products by scrapping the text out of PDF files imported into the program. This allows for a base of knowledge for the program to pull from.
 2. Update connections: The program will use a JSON/Dictionary structure to update connection rules based on user input, i.e if the user wants all n number of workstations to connect to n number of switches.
 3. Convert existing diagrams: In xml2json, this script converts an existing draw.io XML file to JSON. This JSON file is then saved and stored as a 'template' for later use. This program will also update connection rules based on the provided XML file.
    a. While the conversion is occuring, a separate template will be saved in the connections directory. This directory will house all of the geometric data that links each element/node of the diagram. This will allow for future diagrams to be built
       based on information provided by the user. For example, if the user uploads a PDF with an AV architecture, the program will find a template with the best match based on the templates that are stored. This allows for a level of automation to be
       achieved. If there is no template that resembles the information provided, there will be a fallback option to create a template from scratch.
 4. Once the file has been converted and the template saved, the user simply chooses from a templates that has been created, and the json2xml will then convert the JSON template into draw.io XML format.

 I also plan to implement a draw.io docker image that will be used to convert the draw.io xml files into various other formats. Most likely it will be a PDF that I will render in the webapp. This will allow users to see each "template" that is currently
 saved inside the database.


 
