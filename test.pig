traffic = LOAD 'test.csv' using PigStorage();

A = LIMIT traffic 100;

DUMP A;

