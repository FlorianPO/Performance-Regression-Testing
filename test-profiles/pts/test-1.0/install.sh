#!/bin/sh

tar -zxvf bubble_sort.py.tar.gz
echo $? > ~/install-exit-status

echo "#!/bin/sh
python bubble_sort.py > \$LOG_FILE 2>&1
echo \$? > ~/test-exit-status" > bubble_sort
chmod +x bubble_sort
