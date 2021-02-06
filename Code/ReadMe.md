# Feature Extraction
## PACG
### Step 1: Run ICC Analysis
Go to folder `ic3`, follow the steps in README.docx. If mysql is installed, change the Android SDK path, user and password in runic3.sh, and use following command to run:  
`  sh runic3.sh`
### Step 2: PACG Construction
Go to `APKCallGraph.java`, change the paths of Android SDK path, apk file path, and output paths. Compile the project into a `.jar` file, and use the following command to run:  
`  sh runapkcallgraph.sh`

For each app, use the command `python3 getPACG.py` to extract PACGs from apps' call graphs.
## GUI Context
After constructing call graph for each app, DescribeCTX also establish a mapping for activities and their ids. Use `mapping_act_layout.py` to map activities to their corresponding layout files, and use following command to get GUI context:  
`  python3 get_GUI_text.py`
## Permission Description
Use following command to extract permission descriptions from apps' privacy policies:  
`  python3 extract_nlp.py`
