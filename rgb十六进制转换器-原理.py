def rgb_to_hex(r, g, b):
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
        raise ValueError
    return f"#{r:02x}{g:02x}{b:02x}".upper()


rgb_list = []

while True:
    red = input("red>>>")
    green = input("green>>>")
    blue = input("blue>>>")
    if not red == "exit" and not green == "exit" and not blue == "exit":
        R = int(red)
        G = int(green)
        B = int(blue)
        rgb = rgb_to_hex(red, green, blue)
        rgb_list.append(rgb)
        print(rgb_list)
    else:
        break

print(rgb_list)
