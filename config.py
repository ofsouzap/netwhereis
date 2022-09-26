MCAST_ADDR = "239.59.0.1";
PORT = 59016;
MCAST_DST = (MCAST_ADDR, PORT);
MCAST_TTL = 5;

CODE_SIZE = 1;
CODE_FMT = "!b";
CODE_RESPONSE = 0x00;
CODE_SEARCH = 0x01;

# Response format: [CODE (CODE_SIZE bytes)] [RID (RID_SIZE bytes)] [HOSTNAME (HOSTNAME_MAN_LEN bytes)]
# Search format: [CODE (CODE_SIZE bytes)] [RID (RID_SIZE bytes)]

RID_SIZE = 4;
RID_FMT = "!I";

# Maximum number of bytes (and hence ASCII characters) a hostname is allowed to be
HOSTNAME_MAX = 32;

# Maximum amount of data to receive
RECV_BUFFER_SIZE = CODE_SIZE + RID_SIZE + HOSTNAME_MAX;
