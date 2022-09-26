from typing import Tuple, Any;
from struct import pack;
from socket import socket as Socket;
import socket;

from config import *;

def _create_listening_socket() -> Socket:

    sock = Socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP);
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);

    sock.bind(("", PORT));

    mc_req = pack("4sl", socket.inet_aton(MCAST_ADDR), socket.INADDR_ANY);
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mc_req);

    return sock;

def _create_sender_socket() -> Socket:

    sock = Socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP);
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MCAST_TTL);

    return sock;

def recv_broadcast_data() -> Tuple[bytes, Any]:

    sock = _create_listening_socket();
    d, addr = sock.recvfrom(RECV_BUFFER_SIZE);
    sock.close();
    return d, addr;

def broadcast_data(bs: bytes) -> None:

    sock = _create_sender_socket();
    sock.sendto(bs, MCAST_DST);
    sock.close();
