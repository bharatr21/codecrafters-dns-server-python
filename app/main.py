import socket
import struct
from dataclasses import dataclass

@dataclass
class DNSMessage:
    id: int
    qr: int
    opcode: int
    aa: int
    tc: int
    rd: int
    ra: int
    z: int
    rcode: int
    qdcount: int
    ancount: int
    nscount: int
    arcount: int

def create_header(id, qdcount=0):
    return DNSMessage(
        id=id,
        qr=1,
        opcode=0,
        aa=0,
        tc=0,
        rd=0,
        ra=0,
        z=0,
        rcode=0,
        qdcount=qdcount,
        ancount=0,
        nscount=0,
        arcount=0
    )


def pack_dns_message(message: DNSMessage) -> bytes:
    flags = (
        (message.qr << 15)
        | (message.opcode << 11)
        | (message.aa << 10)
        | (message.tc << 9)
        | (message.rd << 8)
        | (message.ra << 7)
        | (message.z << 4)
        | message.rcode
    )

    return struct.pack(
        ">HHHHHH",
        message.id,
        flags,
        message.qdcount,
        message.ancount,
        message.nscount,
        message.arcount,
    )

def main():    
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))
    
    while True:
        try:
            buf, source = udp_socket.recvfrom(512)
            question = buf[12:]
            header = create_header(1234, 1)
            response = pack_dns_message(header) + question
            udp_socket.sendto(response, source)
        except Exception as e:
            print(f"Error receiving data: {e}")
            break


if __name__ == "__main__":
    main()
