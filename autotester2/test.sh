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

PYTHON=python3 ./test.sh >>$logfile 2>&1
ret=$?
echo "return value: $ret" >>$logfile
cat $logfile >>$summary 

cat $basepath/logs/$sha/summary
