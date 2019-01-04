# Setup
 mkfs.jffs2 -x rtime -p -U -b -e 128 -r fs -o fs.bin
 corrupt crc fields in jffs headers of flag node
 wrong inode size field
 overwrite zlib header

# Solution
Fix headers, crc is as simple as:
   def crc(data):
    return (binascii.crc32(data, -1) ^ -1) & 0xffffffff
 jffs2dump -b -e fs.le.bin fs.bin # convert to little endian
 sudo modprobe mtdblock
 sudo modprobe mtdram total_size=16384 erase_size=128
 sudo dd if=fs.le.bin of=/dev/mtdblock0
 sudo mount -t jffs2 /dev/mtdblock0 /mnt

Or carve out zlib data from node and repair magic (compression is 0x6 in jffs2
header, meaning it is zlib)
 dd bs=1 skip=8660080 count=75 if=fs.bin 2>/dev/null | xxd -p | sed '1s/../78/1;1s/../5e/2' | xxd -p -r | zlib-flate -uncompress
