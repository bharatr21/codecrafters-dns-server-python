import socket

def construct_response(buf):
    # Construct response for a DNS header which consists of packet ID of 16 bits, QR = 1, and 0 for the rest, but label each part of the header
    ID = buf[:2]
    QR = b"\x80"
    OPCODE = b"\x00"
    AA = b"\x00"
    TC = b"\x00"
    RD = b"\x00"
    RA = b"\x00"
    Z = b"\x00"
    RCODE = b"\x00"
    QDCOUNT = b"\x00\x00"
    ANCOUNT = b"\x00\x00"
    NSCOUNT = b"\x00\x00"
    ARCOUNT = b"\x00\x00"

    # Construct response for a DNS question which consists of QNAME, QTYPE, and QCLASS, but label each part of the question
    QNAME = buf[12:][:-4]
    QTYPE = b"\x00\x00"
    QCLASS = b"\x00\x00"

    response = ID + QR + OPCODE + AA + TC + RD + RA + Z + RCODE + QDCOUNT + ANCOUNT + NSCOUNT + ARCOUNT + QNAME + QTYPE + QCLASS
    return response


def main():    
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))
    
    while True:
        try:
            buf, source = udp_socket.recvfrom(512)
    
            response = construct_response(buf)
    
            udp_socket.sendto(response, source)
        except Exception as e:
            print(f"Error receiving data: {e}")
            break


if __name__ == "__main__":
    main()
