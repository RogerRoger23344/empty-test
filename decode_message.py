import base64

encoded = "QGVlIWAhb2R2IWdobWQhYmBtbWRlISNVRFJVSE9GL0xFIyFgdSF1aWQhc25udSFuZyF1aWQhc2Rxbi8="
decoded = ''.join(chr(b ^ 0x01) for b in base64.b64decode(encoded))
print(decoded)