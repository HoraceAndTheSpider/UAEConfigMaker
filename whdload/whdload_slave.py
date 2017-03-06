import os
import struct
import binascii
import re
import datetime


class Kickstart:
    def __init__(self, name, crc):
        self.name = name
        self.crc = crc


class WHDLoadSlave:
    _header_offset = 0x020  # 32 bytes
    _flags_dict = {
        1: 'Disk',
        2: 'NoError',
        4: 'EmulTrap',
        8: 'NoDivZero',
        16: 'Req68020',
        32: 'ReqAGA',
        64: 'NoKbd',
        128: 'EmulLineA',
        256: 'EmulTrapV',
        512: 'EmEmulChkul',
        1024: 'EmulPriv',
        2048: 'EmulLineF',
        4096: 'ClearMem',
        8192: 'Examine',
        16384: 'EmulDivZero',
        32768: 'EmulIllegal'
    }

    def __init__(self, path):
        self.path = path
        self.modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(path))
        self.size = None
        self.data_length = None
        self.security = None
        self.id = None
        self.version = None
        self.flags_value = None
        self.base_mem_size = None
        self.exec_install = None
        self.game_loader = None
        self.current_dir_offset = None
        self.dont_cache_offset = None
        self.key_debug = None
        self.key_exit = None
        self.exp_mem = 0
        self.name_offset = None
        self.copy_offset = None
        self.info_offset = None
        self.config_offset = None
        self.current_dir = None
        self.config = [""]
        self.dont_cache = None
        self.name = None
        self.copy = None
        self.info = None
        self.kickstarts = []
        self.kick_name_offset = None
        self.kickstart_size = 0
        self.flags = []
        self._read_data()

    @staticmethod
    def _read_string(offset, data):
        if offset == 0:
            return ""
        length = 0
        for byte in data[offset:]:
            if byte == 0:
                break
            length += 1

        return struct.unpack_from('{}s'.format(length), data[offset:])[0].decode('iso-8859-1')

    def _read_data(self):
        self._get_file_size()

        with open(self.path, 'rb') as f:
            f.seek(self._header_offset, 0)
            _data = bytearray(f.read())

        self._parse_data(_data)
        self._parse_flags()

    def _get_file_size(self):
        self.size = os.path.getsize(self.path)
        self.data_length = self.size - self._header_offset

    def _parse_data(self, data):
        self.security = struct.unpack_from('>L', data[0:])[0]
        self.id = struct.unpack_from('8s', data[4:])[0].decode('iso-8859-1')
        self.version = struct.unpack_from('>H', data[12:])[0]
        self.flags_value = struct.unpack_from('>H', data[14:])[0]
        self.base_mem_size = struct.unpack_from('>L', data[16:])[0]
        self.exec_install = struct.unpack_from('>L', data[20:])[0]
        self.game_loader = struct.unpack_from('>H', data[24:])[0]
        self.current_dir_offset = struct.unpack_from('>H', data[26:])[0]
        self.dont_cache_offset = struct.unpack_from('>H', data[28:])[0]

        _kickstart_crc = 0

        if self.version >= 4:
            self.key_debug = binascii.hexlify(struct.unpack_from('c', data[30:])[0]).decode('iso-8859-1')
            self.key_exit = binascii.hexlify(struct.unpack_from('c', data[31:])[0]).decode('iso-8859-1')

        if self.version >= 8:
            self.exp_mem = struct.unpack_from('>L', data[32:])[0]

        if self.version >= 10:
            self.name_offset = struct.unpack_from('>H', data[36:])[0]
            self.copy_offset = struct.unpack_from('>H', data[38:])[0]
            self.info_offset = struct.unpack_from('>H', data[40:])[0]

        if self.version >= 16:
            self.kick_name_offset = struct.unpack_from('>H', data[42:])[0]
            self.kickstart_size = struct.unpack_from('>L', data[44:])[0]
            _kickstart_crc = struct.unpack_from('>H', data[48:])[0]

        if self.version >= 17:
            self.config_offset = struct.unpack_from('>H', data[50:])[0]

        if self.id != "WHDLOADS":
            raise Exception("Failed to read header: Id is not valid '{}'".format(
                self.id
            ))

        self.current_dir = self._read_string(self.current_dir_offset, data)
        self.dont_cache = self._read_string(self.dont_cache_offset, data)

        if self.version >= 10:
            self.name = self._read_string(self.name_offset, data)
            self.copy = self._read_string(self.copy_offset, data)
            self.info = self._read_string(self.info_offset, data)

        if self.version >= 16:
            if _kickstart_crc == 65535:
                self._parse_multiple_kickstarts(self.kick_name_offset, data)
            elif _kickstart_crc != 0:
                self.kickstarts.append(Kickstart(
                    name=self._read_string(self.kick_name_offset, data),
                    crc=hex(_kickstart_crc)
                ))

        if self.version >= 17:
            self.config = self._read_string(self.config_offset, data).split(';')

    def _parse_multiple_kickstarts(self, offset, data):
        offset_counter = offset
        while True:
            kick_crc = struct.unpack_from('>H', data[offset_counter:])[0]
            if kick_crc == 0:
                break
            offset_counter += 2
            kick_name = self._read_string(struct.unpack_from('>H', data[offset_counter:])[0], data)
            offset_counter += 2
            self.kickstarts.append(Kickstart(
                name=kick_name,
                crc=hex(kick_crc)
            ))

    def _parse_flags(self):
        for key, value in self._flags_dict.items():
            if self.flags_value & key:
                self.flags.append(value)

    def display_data(self):
        print("Path: {}".format(self.path))
        print("Created Time: {}".format(self.modified_time))
        print("WHDLoad Version: {}".format(self.version))
        print("Flags: {}".format(self.flags))
        print("Base Memory Size: {} KiB ({})".format(
            int(self.base_mem_size / 1024),
            hex(self.base_mem_size)
        ))
        print("Current Directory: {}".format(self.current_dir))
        print("Don't Cache: {}".format(self.dont_cache))

        if self.version >= 4:
            print("Debug Key: {}".format(self.key_debug))
            print("Exit Key: {}".format(self.key_exit))

        if self.version >= 8:
            print("Expansion Memory: {} KiB ({})".format(
                int(self.exp_mem / 1024),
                hex(self.exp_mem)
            ))

        if self.version >= 10:
            print("Name: {}".format(self.name))
            print("Copyright: {}".format(self.copy))
            print("Info:")
            info_lines = [line for line in self.info.split('\n') if line.strip() != '']
            for line in info_lines:
                print("\t{}".format(line))

        if self.version >= 16:
            if len(self.kickstarts) > 0:
                print("Kickstarts:")
                for kickstart in self.kickstarts:
                    print("\tName: {}".format(kickstart.name))
                    print("\tCRC: {}".format(kickstart.crc))

                print("Kickstart Size: {} KiB ({})".format(
                    int(self.kickstart_size / 1024),
                    hex(self.kickstart_size)
                ))

        if self.version >= 17:
            print("Config:")
            for config_line in self.config:
                print("\t{}".format(config_line))

    def requires_aga(self):
        return "ReqAGA" in self.flags

    def requires_68020(self):
        return "Req68020" in self.flags

    def has_cd32_controls_patch(self):
        if self.config is not None:
            for config_item in self.config:
                config_item_values = config_item.split(':')
                try:
                    if re.match("^.*[Cc][Dd]32.*$", config_item_values[2]):
                        return True
                except IndexError:
                    pass
        return False


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Parse details of WHDLoad Slave')
    parser.add_argument('--slave', '-s',  # command line argument
                        nargs='*',  # any number of space seperated arguments
                        help='Slave(s) to Scan',
                        )
    args = parser.parse_args()
    slaves_to_scan = args.slave
    for slave_file in slaves_to_scan:
        slave_path = os.path.abspath(slave_file)
        if os.path.isfile(slave_path):
            slave_info = WHDLoadSlave(slave_file)
            slave_info.display_data()
            print('')
        else:
            print("'{}' is not a slave file".format(slave_file))
