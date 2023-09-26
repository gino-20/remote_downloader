#!/bin/bash
PIDFILE=/tmp/rsync.pid
if [ -f $PIDFILE ]; then
    echo "found running rsync, stopping"
    exit 0
fi
touch $PIDFILE
rsync -P -av -e 'ssh -p2022 -i /home/user/trbt_key' --exclude='*.part' --no-owner --omit-dir-times root@45.150.67.232:/downloads/ /c/media/tg_downloads/
rm $PIDFILE