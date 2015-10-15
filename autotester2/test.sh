#!/bin/bash

submit="OFF"
sha=$1
name=$2

basepath=`pwd`

mkdir -p $basepath/logs/$sha
rm -f $basepath/logs/$sha/*

logfile=$basepath/logs/$sha/log
summary=$basepath/logs/$sha/summary

cd $basepath
cd burnman

echo "test: $logfile $summary"
echo "$sha $name at $basepath `date`" >> $logfile

./test.sh >>$logfile 2>&1
ret=$?
echo "return value: $ret" >>$logfile
cat $logfile >>$summary

#grep "ERROR" $logfile >>$summary
#grep "FAIL" $logfile >>$summary
#grep "... ok" $logfile >>$summary

#(
#cd $basepath/aspect/doc/ && exit 0 &&
#make manual.pdf >/dev/null 2>&1 &&
#echo "Manual: OK" || 
#echo "Manual: FAILED";
#git checkout -f -q -- manual.pdf;
#cp manual/manual.log $basepath/logs/$sha/manual.log
#) >>$basepath/logs/$sha/summary
 

cat $basepath/logs/$sha/summary
