f2p_version = {6: '1.1.0',
               5: '0.11.0',
               3: '0.10.0'}


def get_prog_version(version):
    if isinstance(version, int):
        return f2p_version[version]
    else:
        return '0.9.0'


if __name__ == '__main__':
    print(get_prog_version(6))
    print(get_prog_version(0.3))
