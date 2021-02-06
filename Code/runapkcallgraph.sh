for app in `ls ./apks/*.apk`
do
echo $app
java -jar APKCallGraph.jar $app
done
