import cstruct
import sys

class header(cstruct.CStruct):
    __byte_order__ = cstruct.BIG_ENDIAN
    __struct__ = """
        uint16_t magic;
        uint16_t nodetype;
        uint32_t totlen; /* So we can skip over nodes we don't grok */
        uint32_t hdr_crc;
    """

class inode(cstruct.CStruct):
    __byte_order__ = cstruct.BIG_ENDIAN
    __struct__ = """
        uint16_t magic;      /* A constant magic number.  */
        uint16_t nodetype;   /* == JFFS2_NODETYPE_INODE */
        uint32_t totlen;     /* Total length of this node (inc data, etc.) */
        uint32_t hdr_crc;
        uint32_t ino;        /* Inode number.  */
        uint32_t version;    /* Version number.  */
        uint32_t mode;       /* The file's type or mode.  */
        uint16_t uid;        /* The file's owner.  */
        uint16_t gid;        /* The file's group.  */
        uint32_t isize;      /* Total resultant size of this inode (used for truncations)  */
        uint32_t atime;      /* Last access time.  */
        uint32_t mtime;      /* Last modification time.  */
        uint32_t ctime;      /* Change time.  */
        uint32_t offset;     /* Where to begin to write.  */
        uint32_t csize;      /* (Compressed) data size */
        uint32_t dsize;      /* Size of the node's data. (after decompression) */
        uint8_t compr;       /* Compression algorithm used */
        uint8_t usercompr;   /* Compression algorithm requested by the user */
        uint16_t flags;      /* See JFFS2_INO_FLAG_* */
        uint32_t data_crc;   /* CRC for the (compressed) data.  */
        uint32_t node_crc;   /* CRC for the raw inode (excluding data)  */
        /*__u8 data[0];*/
    """

def pad(x):
    return (((x) + 3) & ~3)

with open(sys.argv[1], "rb") as f:
    header = header()
    inode = inode()
    while True:
        buf = f.read(len(header))
        if f.tell() % 0x1000000 == 0: print hex(f.tell())
        if buf == '': break
        header.unpack(buf)
        if header.magic != 0x1985:
            f.seek(-len(header) + 1, 1)
            continue
        if header.nodetype == 0xe002:
            buf += f.read(pad(header.totlen) - len(header))
            inode.unpack(buf[:len(inode)])
            if inode.mode != 0x81b4:
                print chr(int(hex(inode.mode)[2:4], 16)),


