def create_packet(command, data):
    packet = bytes([
        0xAA,
        command,
        *data,
        0x55
    ])

    return packet