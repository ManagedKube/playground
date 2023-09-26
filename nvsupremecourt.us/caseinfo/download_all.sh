#!/bin/bash

## This script has a variable that is a number named: csIID
## It will create a loop and in each loop iteration it will
## go to this URL https://caseinfo.nvsupremecourt.us/public/caseView.do?csIID=${csIID}
## and download the HTML file to the directory where this script is located.
## Then it will increment the ${csIID}} variable by 1 and repeat the process.
## It will do this until it reaches the number 1000000.

csIID=1
maxCSIID=4
outputFolder="./outputs"

while [ $csIID -lt $maxCSIID ]
do
    wget https://caseinfo.nvsupremecourt.us/public/caseView.do?csIID=${csIID} -P $outputFolder
    csIID=$(( $csIID + 1 ))
done
