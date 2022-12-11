import struct

name = input()
with open(name, 'rb') as f:
    data = f.read()

    if data[8:12] == b'WAVE' or len(data) < 44:
        try:
            print(f'Size={struct.unpack("=i", data[4:8])} Type={struct.unpack("=h",data[20:22])} Channels={struct.unpack("=h", data[22:24])} Rate={struct.unpack("=i",data[24:28])} Bits={struct.unpack("=h", data[34:36])} Data size={struct.unpack("=i", data[40:44])}'.replace(')', '').replace('(', '')[:-1])
        except Exception:
            print('NO')
    else:
        print('NO')