from bleak import BleakScanner
from bleak_winrt.windows.devices import bluetooth
from bleak_winrt.windows.devices.bluetooth import BluetoothLEDevice
from bleak_winrt.windows.devices.enumeration import DevicePairingKinds, DevicePairingResultStatus

async def find_devices():
    scanner = BleakScanner()
    devices = await scanner.discover()

    nearby_devices = [(device.address, device.name) for device in devices]
    return nearby_devices

async def pair_device(address):
    device = await BluetoothLEDevice.from_ble_device_id_async(address)
    if device:
        custom_pairing = device.device_information.pairing.custom
        pair_kind = DevicePairingKinds.CONFIRM_ONLY

        result = await custom_pairing.pair_async(pair_kind)
        if result.status == DevicePairingResultStatus.PAIRED:
            return True, "Device paired successfully."
        else:
            return False, f"Device pairing failed. Status: {result.status}"
    else:
        return False, "Unable to connect to the device."


def parse_data(data):
    data_dict = {}
    for item in data.split(','):
        key, value = item.split(':')
        data_dict[key] = value
    return data_dict

def connect_device(nearby_devices, index):
    # 사용자가 선택한 기기 연결
    address, name = nearby_devices[index]
    print(f"Connecting to {name} - {address}")

    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((address, 1))

    # 데이터 수신 및 파싱
    data = sock.recv(1024).decode('utf-8')
    parsed_data = parse_data(data)
    print("Received data:", parsed_data)

    sock.close()
    return parsed_data
