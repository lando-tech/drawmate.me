drawmate.me:
  
  About:




  Modules:
    
    xml2json:
        
        To be facilitate creating templates based on previous diagrams/wiremaps, this module uses an
        algorithm to convert a drawio.xml file into a python dict, and then writes the dict to a JSON
        file in order to store the template. To initialize the xml2json class, you must pass in a path
        to the xml file, or optionally in main.py there is a simple cli prompt that uses the tkinter
        filedialog to allow the user to use their native file explorer to navigate and find the xml file.
        With the filepath specified, you can then call the 'write_json' function and specify the name of 
        the new template. It will then write the template to disk and create an additional JSON file 
        labled templates   
                

    json2xml: This module is the main algorithm that converts a JSON file to a useable drawio.xml file.


    pdf_handler:

    pathfinder:

    config:

    db:

    update:

    app:

    cli:
