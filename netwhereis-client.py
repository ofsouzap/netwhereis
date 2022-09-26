from struct import pack, unpack;
import struct;
import random;
from io import BytesIO;

from config import *;
import network;

def generate_rid() -> int:
    return random.randint(0, 1 << RID_SIZE - 1);

def generate_search_request(rid: int) -> bytes:

    bs = bytearray();
    bs += pack(CODE_FMT, CODE_SEARCH);
    bs += pack(RID_FMT, rid);

    return bytes(bs);

def main():

    # Generate RID
    req_rid = generate_rid();

    # Send request
    req = generate_search_request(req_rid);
    network.broadcast_data(req);

    # Listen for responses until interrupted

    try:

        while True:

            d, addr = network.recv_broadcast_data();

            stream = BytesIO(d);

            try:

                code: int = unpack(CODE_FMT, stream.read(CODE_SIZE))[0];

                if code == CODE_RESPONSE:

                    rid = unpack(RID_FMT, stream.read(RID_SIZE))[0];

                    if rid == req_rid:

                        hostname = stream.read(HOSTNAME_MAX).decode().strip(" ");

                        print(f"{hostname} is at {addr}");

            except struct.error:
                pass;

    except KeyboardInterrupt:
        print("Stopping listening for responses.");

if __name__ == "__main__":
    main();
