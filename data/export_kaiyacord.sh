#!/bin/bash
# Info: https://github.com/Tyrrrz/DiscordChatExporter/blob/master/.docs

TOKEN=MjIxMTE3ODAyMjY4ODUyMjI2.GP76oq.Q1jAzGC-3OfJ-0sr-brEFHqNz3aB8FN3i65stA
CHANNELID=1038808890466390066
# DLLFOLDER=/run/media/data_day_life/Vault/Coding_Projects/CountletBot/src/data/DiscordChatExporter.Cli
FILENAME='Kaiyacord - the-quest-to-10k'
EXPORTDIRECTORY=/run/media/data_day_life/Vault/Coding_Projects/CountletBot/src/data_cold_start
EXPORTFORMAT=json
# Available export formats: plaintext, htmldark, htmllight, json, csv
# /\ CaSe-SeNsItIvE /\
# You can edit the export command on line 40 if you'd like to include more options like date ranges and date format. You can't use partitioning (-p) with this script.

# This will verify if EXPORTFORMAT is valid and will set the final file extension according to it. If the format is invalid, the script will display a message and exit.
if [[ "$EXPORTFORMAT" == "plaintext" ]]; then
FORMATEXT=.txt
elif [[ "$EXPORTFORMAT" == "htmldark" ]] || [[ "$EXPORTFORMAT" == "htmllight" ]]; then
FORMATEXT=.html
elif [[ "$EXPORTFORMAT" == "json" ]]; then
FORMATEXT=.json
elif [[ "$EXPORTFORMAT" == "csv" ]]; then
FORMATEXT=.csv
else
echo "$EXPORTFORMAT - Unknown export format"
echo "Available export formats: plaintext, htmldark, htmllight, csv, json"
echo "/\ CaSe-SeNsItIvE /\\"
exit 1
fi

# # This will change the script's directory to DLLPATH, if unable to do so, the script will exit.
# cd $DLLFOLDER || exit 1

# This will export your chat
# dotnet DiscordChatExporter.Cli.dll export -t $TOKEN -c $CHANNELID -f $EXPORTFORMAT -o $FILENAME.tmp
# discord-chat-exporter-cli export -t $TOKEN -c $CHANNELID -f $EXPORTFORMAT -o $FILENAME.tmp
discord-chat-exporter-cli export -t $TOKEN -c $CHANNELID -f $EXPORTFORMAT

# This sets the current time to a variable
CURRENTTIME=$(date +"%Y-%m-%d-%H-%M-%S")

# This will move the .tmp file to the desired export location, if unable to do so, it will attempt to delete the .tmp file.
if ! mv "$FILENAME.tmp" "${EXPORTDIRECTORY//\"}/$FILENAME-$CURRENTTIME$FORMATEXT" ; then
echo "Unable to move $FILENAME.tmp to $EXPORTDIRECTORY/$FILENAME-$CURRENTTIME$FORMATEXT."
echo "Cleaning up..."
  if ! rm -Rf "$FILENAME.tmp" ; then
  echo "Unable to remove $FILENAME.tmp."
  fi
exit 1
fi
exit 0