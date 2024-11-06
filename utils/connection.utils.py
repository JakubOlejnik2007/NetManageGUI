from NetManage.utils import COM_CONNECTION, SSHTEL_CONNECTION, TFTP_CONNECTION


def testConnection(connection: COM_CONNECTION | SSHTEL_CONNECTION | TFTP_CONNECTION):
    connect = connection.getNetmikoConnDict()


