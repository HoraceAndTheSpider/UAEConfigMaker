import os
import struct
import binascii


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
        self.size = None
        self.data_length = None
        self.data = None
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
        self.exp_mem = None
        self.name_offset = None
        self.copy_offset = None
        self.info_offset = None
        self.kick_name_offset = None
        self.kickstart_size = None
        self.kickstart_crc = None
        self.config_offset = None
        self.current_dir = None
        self.config = None
        self.dont_cache = None
        self.name = None
        self.copy = None
        self.info = None
        self.kickstart_name = None
        self.flags = []
        self._read_data()

    def _read_data(self):
        self._get_file_size()

        with open(self.path, 'rb') as f:
            f.seek(self._header_offset, 0)
            self.data = bytearray(f.read())

        self._parse_data()
        self._parse_flags()

    def _get_file_size(self):
        self.size = os.path.getsize(self.path)
        self.data_length = self.size - self._header_offset

    def _parse_data(self):
        self.security = struct.unpack_from('>L', self.data[0:])[0]
        self.id = struct.unpack_from('8s', self.data[4:])[0].decode('iso-8859-1')
        self.version = struct.unpack_from('>H', self.data[12:])[0]
        self.flags_value = struct.unpack_from('>H', self.data[14:])[0]
        self.base_mem_size = struct.unpack_from('>L', self.data[16:])[0]
        self.exec_install = struct.unpack_from('>L', self.data[20:])[0]
        self.game_loader = struct.unpack_from('>H', self.data[24:])[0]
        self.current_dir_offset = struct.unpack_from('>H', self.data[26:])[0]
        self.dont_cache_offset = struct.unpack_from('>H', self.data[28:])[0]
        self.key_debug = binascii.hexlify(struct.unpack_from('c', self.data[30:])[0]).decode('iso-8859-1')
        self.key_exit = binascii.hexlify(struct.unpack_from('c', self.data[31:])[0]).decode('iso-8859-1')
        self.exp_mem = struct.unpack_from('>L', self.data[32:])[0]
        self.name_offset = struct.unpack_from('>H', self.data[36:])[0]
        self.copy_offset = struct.unpack_from('>H', self.data[38:])[0]
        self.info_offset = struct.unpack_from('>H', self.data[40:])[0]
        self.kick_name_offset = struct.unpack_from('>H', self.data[42:])[0]
        self.kickstart_size = struct.unpack_from('>L', self.data[44:])[0]
        self.kickstart_crc = hex(struct.unpack_from('>H', self.data[48:])[0])
        self.config_offset = struct.unpack_from('>H', self.data[50:])[0]

        if self.id != "WHDLOADS":
            raise Exception("Failed to read header: Id is not valid '{}'".format(
                self.id
            ))

        self.current_dir = self._read_string(self.current_dir_offset)
        self.dont_cache = self._read_string(self.dont_cache_offset)

        if self.version >= 10:
            self.name = self._read_string(self.name_offset)
            self.copy = self._read_string(self.copy_offset)
            self.info = self._read_string(self.info_offset)

        if self.version >= 16:
            self.kickstart_name = self._read_string(self.kick_name_offset)

        if self.version >= 17:
            self.config = self._read_string(self.config_offset)

    def _read_string(self, offset):
        if offset == 0:
            return ""
        length = 0
        for byte in self.data[offset:]:
            if byte == 0:
                break
            length += 1

        return struct.unpack_from('{}s'.format(length), self.data[offset:])[0].decode('iso-8859-1')

    def _parse_flags(self):
        for key, value in self._flags_dict.items():
            if self.flags_value & key:
                self.flags.append(value)

    def display_data(self):
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
            print("Kickstart Name: {}".format(self.kickstart_name))
            print("Kickstart Size: {} KiB ({})".format(
                int(self.kickstart_size / 1024),
                hex(self.kickstart_size)
            ))
            print("Kickstart CRC: {}".format(self.kickstart_crc))

    def requires_aga(self):
        return "ReqAGA" in self.flags

    def requires_68020(self):
        return "Req68020" in self.flags

