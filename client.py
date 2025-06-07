import socket
import struct
import time
from XInput import get_state

UDP_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Remote Controller Client")
UDP_IP = "10.0.0.1"

PLAYER_NUMBER = 2

print(f"Client started for player {PLAYER_NUMBER}, sending to {UDP_IP}:{UDP_PORT}")

def pack_state(player_num):
    try:
        state = get_state(0)
        gp = state.Gamepad
    except:
        return None
    packet = struct.pack(
        '<B H B B h h h h',
        player_num,
        gp.wButtons,
        gp.bLeftTrigger,
        gp.bRightTrigger,
        gp.sThumbLX,
        gp.sThumbLY,
        gp.sThumbRX,
        gp.sThumbRY
    )
    return packet

while True:
    try:
        while True:
            packet = pack_state(PLAYER_NUMBER)
            if packet != None:
                sock.sendto(packet, (UDP_IP, UDP_PORT))
                print(packet)
            time.sleep(1/60)
    except:
        print("Client terminated.")
