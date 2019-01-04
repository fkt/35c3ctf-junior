# Setup
 mkfs.jffs2 -x rtime -p -U -b -e 128 -r fs -o fs.bin

# Solution
 jffs2dump -b -e fs.le.bin fs.bin # convert to little endian
 sudo modprobe mtdblock
 sudo modprobe mtdram total_size=16384 erase_size=128
 sudo dd if=fs.le.bin of=/dev/mtdblock0
 sudo mount -t jffs2 /dev/mtdblock0 /mnt
