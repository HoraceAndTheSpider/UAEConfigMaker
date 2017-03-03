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
        self.Path = path
        self.Size = None
        self.DataLength = None
        self.Data = None
        self.Security = None
        self.Id = None
        self.Version = None
        self.FlagsValue = None
        self.BaseMemSize = None
        self.ExecInstall = None
        self.GameLoader = None
        self.CurrentDirOffset = None
        self.DontCacheOffset = None
        self.KeyDebug = None
        self.KeyExit = None
        self.ExpMem = None
        self.NameOffset = None
        self.CopyOffset = None
        self.InfoOffset = None
        self.KickNameOffset = None
        self.KickSize = None
        self.KickCRC = None
        self.ConfigOffset = None
        self.CurrentDir = None
        self.Config = None
        self.DontCache = None
        self.Name = None
        self.Copy = None
        self.Info = None
        self.KickstartName = None
        self.Flags = []
        self._read_data()

    def _read_data(self):
        self._get_file_size()

        with open(self.Path, 'rb') as f:
            f.seek(self._header_offset, 0)
            self.Data = bytearray(f.read())

        self._parse_data()
        self._parse_flags()

    def _get_file_size(self):
        self.Size = os.path.getsize(self.Path)
        self.DataLength = self.Size - self._header_offset

    def _parse_data(self):
        self.Security = struct.unpack_from('>L', self.Data[0:])[0]
        self.Id = struct.unpack_from('8s', self.Data[4:])[0].decode('iso-8859-1')
        self.Version = struct.unpack_from('>H', self.Data[12:])[0]
        self.FlagsValue = struct.unpack_from('>H', self.Data[14:])[0]
        self.BaseMemSize = struct.unpack_from('>L', self.Data[16:])[0]
        self.ExecInstall = struct.unpack_from('>L', self.Data[20:])[0]
        self.GameLoader = struct.unpack_from('>H', self.Data[24:])[0]
        self.CurrentDirOffset = struct.unpack_from('>H', self.Data[26:])[0]
        self.DontCacheOffset = struct.unpack_from('>H', self.Data[28:])[0]
        self.KeyDebug = binascii.hexlify(struct.unpack_from('c', self.Data[30:])[0]).decode('iso-8859-1')
        self.KeyExit = binascii.hexlify(struct.unpack_from('c', self.Data[31:])[0]).decode('iso-8859-1')
        self.ExpMem = struct.unpack_from('>L', self.Data[32:])[0]
        self.NameOffset = struct.unpack_from('>H', self.Data[36:])[0]
        self.CopyOffset = struct.unpack_from('>H', self.Data[38:])[0]
        self.InfoOffset = struct.unpack_from('>H', self.Data[40:])[0]
        self.KickNameOffset = struct.unpack_from('>H', self.Data[42:])[0]
        self.KickSize = struct.unpack_from('>L', self.Data[44:])[0]
        self.KickCRC = hex(struct.unpack_from('>H', self.Data[48:])[0])
        self.ConfigOffset = struct.unpack_from('>H', self.Data[50:])[0]

        if self.Id != "WHDLOADS":
            raise Exception("Failed to read header: Id is not valid '{}'".format(
                self.Id
            ))

        self.CurrentDir = self._read_string(self.CurrentDirOffset)
        self.DontCache = self._read_string(self.DontCacheOffset)

        if self.Version >= 10:
            self.Name = self._read_string(self.NameOffset)
            self.Copy = self._read_string(self.CopyOffset)
            self.Info = self._read_string(self.InfoOffset)

        if self.Version >= 16:
            self.KickstartName = self._read_string(self.KickNameOffset)

        if self.Version >= 17:
            self.Config = self._read_string(self.ConfigOffset)

    def display_data(self):
        print("WHDLoad Version: {}".format(self.Version))
        print("Flags: {}".format(self.Flags))
        print("Base Memory Size: {} KiB ({})".format(
            int(self.BaseMemSize / 1024),
            hex(self.BaseMemSize)
        ))
        print("Current Directory: {}".format(self.CurrentDir))
        print("Don't Cache: {}".format(self.DontCache))

        if self.Version >= 4:
            print("Debug Key: {}".format(self.KeyDebug))
            print("Exit Key: {}".format(self.KeyExit))

        if self.Version >= 8:
            print("Expansion Memory: {} KiB ({})".format(
                int(self.ExpMem / 1024),
                hex(self.ExpMem)
            ))

        if self.Version >= 10:
            print("Name: {}".format(self.Name))
            print("Copyright: {}".format(self.Copy))
            print("Info:")
            info_lines = [line for line in self.Info.split('\n') if line.strip() != '']
            for line in info_lines:
                print("\t{}".format(line))

        if self.Version >= 16:
            print("Kickstart Name: {}".format(self.KickstartName))
            print("Kickstart Size: {} KiB ({})".format(
                int(self.KickSize / 1024),
                hex(self.KickSize)
            ))
            print("Kickstart CRC: {}".format(self.KickCRC))

    def _read_string(self, offset):
        if offset == 0:
            return ""
        length = 0
        for byte in self.Data[offset:]:
            if byte == 0:
                break
            length += 1

        return struct.unpack_from('{}s'.format(length), self.Data[offset:])[0].decode('iso-8859-1')

    def _parse_flags(self):
        for key, value in self._flags_dict.items():
            if self.FlagsValue & key:
                self.Flags.append(value)

