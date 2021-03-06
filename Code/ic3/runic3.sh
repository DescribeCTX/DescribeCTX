#! /bin/sh

appDir=$1
forceAndroidJar=./android-18/android.jar

var=1
for appPath in `ls $appDir/*.apk`
do
appName=`basename $appPath .apk`
retargetedPath=testspace/$appName.apk

mysql -uroot -p<password> -e 'drop database if exists cc; create database cc'
mysql -uroot -p<password> cc < schema

mkdir output/$appName

gtimeout 1800 java -Xmx24000m -jar RetargetedApp.jar $forceAndroidJar $appPath $retargetedPath
gtimeout 1800 java -Xmx24000m -jar ic3-0.2.0-full.jar -apkormanifest $appPath -input $retargetedPath -cp $forceAndroidJar -db cc.properties -dbname cc1 -protobuf output/$appName
var=$((var+1))
done
echo "finished $var apk files."
