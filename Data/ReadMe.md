# Description
## Apps
All data used in DescribeCTX is listed in apps.txt. In total there are 8814 apps we examined and we present the data in their package names. Please go to AndroZoo to download the .apk files. Please get MD5 for each app before downloading, the MD5 can also be obtained on AndroZoo. For details, please go https://androzoo.uni.lu/.
## Data
The extracted triples (i.e. permission description-GUI context-PACG) with its corresponding reference sentences is in data.csv file. The last column represents the corresponding permissions.  
1st column: apps' permission descriptions extracted from their privacy policies.  
2nd column: apps' GUI contextual text extracted from their layout files.  
3rd column: text from apps' PACG, i.e. tokenized method names. For example, method ***getLastKnownLocation()*** is extracted as ***get last known location***.  
4th column: indicate the apps' permission group, i.e. ***CONTACT***, ***LOCATION***, ***CAMERA***, ***SMS***, ***CALENDAR***, ***STORAGE***, and ***MICROPHONE***. Note that an app may require several sensitive permssions. Therefore, it may appear in multiple permission groups.
