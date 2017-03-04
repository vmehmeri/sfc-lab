import os

DC1_IP='10.0.0.1'
DC2_IP='10.0.0.2'
DC1_IP2='11.0.0.1'
DC2_IP2='11.0.0.2'



DC1_MAC='08:00:11:11:11:11'
DC2_MAC='08:00:22:22:22:22'



def setStaticArp():

    os.system( "ssh vime@dc2 sudo arp -s %s %s -i eth2" %(DC2_IP,DC2_MAC) )
    os.system( "ssh vime@dc2 sudo arp -s %s %s -i eth2" %(DC2_IP2,DC2_MAC) )


    os.system( "ssh vime@dc1 sudo arp -s  %s %s -i eth2" %(DC1_IP, DC1_MAC) )
    os.system( "ssh vime@dc1 sudo arp -s  %s %s -i eth2" %(DC1_IP2, DC1_MAC) )

    #os.system( "ssh fla@tnt1vno1-client sudo arp -s %s %s -i eth1" %(TNT1VNO1_SERVER_IP, TNT1VNO1_SERVER_MAC) )
    #os.system( "ssh fla@tnt1vno1-server sudo arp -s %s %s -i eth1" %(TNT1VNO1_CLIENT_IP, TNT1VNO1_CLIENT_MAC) )
    #os.system( "ssh fla@tnt1vno2-client sudo arp -s %s %s -i eth1" %(TNT1VNO2_SERVER_IP, TNT1VNO2_SERVER_MAC) )
    #os.system( "ssh fla@tnt1vno2-server sudo arp -s %s %s -i eth1" %(TNT1VNO2_CLIENT_IP, TNT1VNO2_CLIENT_MAC) )
    #os.system( "ssh fla@tnt2vno1-client sudo arp -s %s %s -i eth1" %(TNT2VNO1_SERVER_IP, TNT2VNO1_SERVER_MAC) )
    #os.system( "ssh fla@tnt2vno1-server sudo arp -s %s %s -i eth1" %(TNT2VNO1_CLIENT_IP, TNT2VNO1_CLIENT_MAC) )

    #os.system( "ssh fla@sff-vm2 sudo arp -s %s %s -i eth1" %(FLA_SERVER1_IP, FLA_SERVER1_MAC) )
    #os.system( "ssh fla@sff-vm2 sudo arp -s %s %s -i eth1" %(FLA_SERVER3_IP, FLA_SERVER3_MAC) )
    #os.system( "ssh fla@sff-vm2 sudo arp -s %s %s -i eth1" %(SFF1_IP, SFF1_MAC) )

if __name__ == "__main__":
    setStaticArp()
