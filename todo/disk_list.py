import subprocess
from pprint import pprint

def execute_command(command):
    """
    Executes a command in the command line and captures the output.

    Args:
    command (str): Command to be executed.

    Returns:
    str: The output of the command.
    """
    result = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return result.stdout



def parse_disk_info(raw_data):
    """
    Parses 'key=value' formatted disk data into a list of dictionaries.

    `raw_data` example:
    ```
    DeviceID=\\.\PHYSICALDRIVE0
    Model=SanDisk SD8SN8U-256G-1006
    SerialNumber=164212802559
    Size=256052966400

    DeviceID=\\.\PHYSICALDRIVE1
    Model=Generic EF8S5 SD Card
    SerialNumber=52f25fae
    Size=512706378240

    DeviceID=\\.\PHYSICALDRIVE2
    Model=SDXC Card
    SerialNumber=
    Size=512706378240
    ```

    Args:
    raw_data (str): Raw string output from the command line.

    Returns:
    list of dict: List of dictionaries with parsed disk information.
    """
    # Разделяем данные по переводам строки, каждый блок представляет один диск
    blocks = raw_data.strip().split("\n\n\n")
    disks = []
    for block in blocks:
        disk_info = {}
        # Разбираем каждую строку в блоке
        for line in block.split('\n'):
            if line.strip():
                key, value = line.split('=', 1)
                disk_info[key.strip()] = value.strip()

        # Добавляем диск только если нашли данные
        if disk_info:
            if 'Size' in disk_info and disk_info['Size'].isdigit():
                disk_info['Size'] = int(disk_info['Size'])
                disk_info['SizeGB'] = round(disk_info['Size'] / (1024**3), 3)
                disk_info['SizeStrGB'] = f"{disk_info['SizeGB']:.2f} GB"
            disks.append(disk_info)
    return disks

# Command to get disk drive information in 'value' format
disk_info_command = "wmic diskdrive get deviceid, model, size, serialnumber /format:value"

# Execute the command and parse the data
disk_info = execute_command(disk_info_command)
disks = parse_disk_info(disk_info)

# Print disk information
for disk in disks:
    pprint(disk)
