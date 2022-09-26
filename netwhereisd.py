from struct import pack, unpack;
import struct;
import logging;
from io import BytesIO;
import socket
from typing import Any;

from config import *;
import network;

LOG_FILE = "log";
TIMEOUT = 1;

def generate_search_response(rid: int) -> bytes:

    # Get hostname
    hostname = socket.gethostname();

    # Extend hostname if needed
    while len(hostname) < HOSTNAME_MAX:
        hostname = hostname + " ";

    # Crop hostname if needed
    hostname = hostname[:HOSTNAME_MAX];

    # Encode hostname
    hostname_bs = hostname.encode();

    # Return bytes
    bs = bytearray();
    bs += pack(CODE_FMT, CODE_RESPONSE);
    bs += pack(RID_FMT, rid);
    bs += hostname_bs;
    return bytes(bs);

def handle_req_search(stream: BytesIO,
    addr: Any) -> None:

    rid: int = unpack(RID_FMT, stream.read(RID_SIZE))[0];

    response = generate_search_response(rid);

    network.broadcast_data(response);

    logging.info(f"Handled search request from {addr}");

def main() -> None:

    # Prepare logging
    logging.basicConfig(
        filename = LOG_FILE,
        level = logging.INFO,
        format = "%(asctime)s - %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S"
    );

    # Main loop

    while True:

        d, addr = network.recv_broadcast_data();

        stream = BytesIO(d);

        try:

            code: int = unpack(CODE_FMT, stream.read(CODE_SIZE))[0];

            if code == CODE_RESPONSE:
                logging.info(f"Response heard from {addr}.");

            elif code == CODE_SEARCH:
                handle_req_search(stream, addr);
                logging.info(f"Search request received from {addr}");

            else:
                logging.info(f"Unknown data code ({hex(code)}) received from {addr}");

        except struct.error:
            logging.info(f"Erroneous data from {addr}.");

if __name__ == "__main__":
    main();