import socket
import struct
import vgamepad as vg

# Virtual gamepads for players 2, 3, and 4
gamepads = {
    2: vg.VX360Gamepad(),
    3: vg.VX360Gamepad(),
    4: vg.VX360Gamepad()
}

# Server setup
UDP_IP = '0.0.0.0'
UDP_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Server running and waiting for input...")

BUTTON_MAPPING = {
    0x0001: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
    0x0002: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
    0x0004: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
    0x0008: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
    0x0010: vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
    0x0020: vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
    0x0040: vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
    0x0080: vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
    0x0100: vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
    0x0200: vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
    0x1000: vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
    0x2000: vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
    0x4000: vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
    0x8000: vg.XUSB_BUTTON.XUSB_GAMEPAD_Y
}

def parse_packet(data):
    unpacked = struct.unpack('<B H B B h h h h', data)
    return {
        'player': unpacked[0],
        'buttons': unpacked[1],
        'left_trigger': unpacked[2],
        'right_trigger': unpacked[3],
        'lx': unpacked[4],
        'ly': unpacked[5],
        'rx': unpacked[6],
        'ry': unpacked[7],
    }

def apply_state(pad:vg.VX360Gamepad, state):

    print(state)
    pad.reset()
    
    # Buttons
    for bitmask, button in BUTTON_MAPPING.items():
        if state['buttons'] & bitmask:
            pad.press_button(button)
    
    # Triggers
    pad.left_trigger(state['left_trigger'])
    pad.right_trigger(state['right_trigger'])
    
    # Joysticks
    pad.left_joystick(state['lx'], state['ly'])
    pad.right_joystick(state['rx'], state['ry'])
    
    pad.update()

while True:
    data, addr = sock.recvfrom(1024)
    if len(data) == 13:  # Ensure correct packet size
        state = parse_packet(data)
        player = state['player']
        if player in gamepads:
            apply_state(gamepads[player], state)
            print(f"Updated Player {player} from {addr}")
