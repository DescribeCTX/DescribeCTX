# PACG

## Step 1: Run ICC Analysis

Navigate to the `ic3` folder. Inside `runic3.sh`, update the Android SDK path and version to match your setup. If you have MySQL installed, modify the user and password settings in `runic3.sh`. Before executing `runic3.sh` for the first time, create an output directory using the `mkdir output` command.

### Detailed Steps:
1. Change `forceAndroidJar=../android-22/android.jar` to point to your specific Android SDK version.
2. If you haven't already, install MySQL. Next, navigate to the `cc.properties` file and update the user and password fields.
3. Execute `ic3.sh` with the following command: `sh runic3.sh <APK_Directory>`

If some of your `.apk` files failed to generate outputs, check the log. If your environment is setup correctly, the primary issue may be caused by the Android SDK version that you claim in `runic3.sh`. Double-check it.

By default settings, this step will give you a `.txt` for each apk, which are placed in the `./output` directory.

## Step 2: PACG Construction

Navigate to `APKCallGraph.java` and update the following paths:
- Android SDK path: Adjust the `static String androidPlatformPath` to point to your SDK location.
- APK file path: Modify the `String apkPath`. By default, it will use APKs located in `./apks`.
- Output paths: Update the paths at `File mappingfile = new File("./activity_id_mapping/" + apk + ".txt");` and `File file = new File("./dot_output/" + apk + "/");`.
- If you've specified a custom path for ic3's outputs in the previous step, also change the path at `String ic3 = "./ic3/output/"`.

Next, compile the project into a `.jar` file. Copy `SourcesAndSinks.txt` and `AndroidCallbacks.txt` to the same directory as `runapkcallgraph.sh`. Then, execute the script using:
`  sh runapkcallgraph.sh`

This step will produce call graphs in `.dot` format and activity_id_mapping in `.txt` format.

Finally, execute the following command to extract PACGs from the app call graphs:
`  python3 getPACG.py`

Before running `getPACG.py`, make the following adjustments:
- Update the app names input path at `apps = os.listdir('./Descriptions/Contacts/')`.
- Modify the `.dot` graph path (generated in the previous step) – by default, it's set to `dot_dir = './APKCallGraph/dot_output/'`.
- Specify the `sensitive api call` at Line37: `enter sensitive API here` Refer to the [Android Developer website](https://developer.android.com/reference/android/location/LocationManager#public-methods) for details.
- Specify your desired output path.

**Note**: Ensure that the app names in your specified input path match the names of the .dot files in the graph path.

## GUI Context

### Step 1:
This step will also use the outputs from APKTool, use `apk d xxx.apk` to decode the apks.
For more details, refer to [Decoding | Apktool](https://ibotpeaches.github.io/Apktool/documentation/).

### Step 2:
After constructing a call graph for each app, DescribeCTX also establishes a mapping for activities and their ids. Use `mapping_act_layout.py` to associate activities with their corresponding layout files.

In `mapping_act_layout.py`, specify the following two paths:
- `resourcedir = './demo/apktool_output/'`
- `mappingdir = './demo/activity_id_mapping/'`

The `resourcedir` is the output path from `apktool`, while `mappingdir` is the output path from the previous `sh runapkcallgraph.sh` step.

### Step 3:
To retrieve the GUI context, use the following command:
`  python3 get_GUI_text.py`

Make the following modifications in `get_GUI_text.py`:
- Update the path for your APK list on line 89 (`app_dir`).
- Modify the path on line 39 to point to your outputs from Step 2.
- Adjust the path on line 58 (`apk_res_dir`) to the `apktool` output path.

## Permission Description

Use the following command to extract permission descriptions from apps' privacy policies:
`  python3 extract_pp.py`

**Note**:
As Soot doesn’t support newer SDK versions at this point. We recommend you to use the SDK version between 18 to 22. At the same time, pay attention to the SDK version corresponding to the APKs.
