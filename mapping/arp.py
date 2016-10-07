import os

FLA_SERVER1_IP='10.0.0.1'
FLA_SERVER3_IP='10.0.0.2'
FLA_SERVER1_IP2='11.0.0.1'
FLA_SERVER3_IP2='11.0.0.2'

TNT1VNO1_CLIENT_IP='10.0.0.10'
TNT1VNO1_SERVER_IP='10.0.0.20'
TNT1VNO2_CLIENT_IP='10.0.0.10'
TNT1VNO2_SERVER_IP='10.0.0.20'
TNT2VNO1_CLIENT_IP='11.0.0.10'
TNT2VNO1_SERVER_IP='11.0.0.20'

#SFF2_IP='10.0.0.4'
#H1_IP='10.0.0.10'
#H2_IP='10.0.0.20'

FLA_SERVER1_MAC='00:1b:21:a6:8f:fd'
FLA_SERVER3_MAC='00:1b:21:a6:90:1f'


TNT1VNO1_CLIENT_MAC='aa:aa:aa:22:22:22'
TNT1VNO1_SERVER_MAC='aa:aa:aa:44:44:44'
TNT1VNO2_CLIENT_MAC='aa:aa:aa:33:33:33'
TNT1VNO2_SERVER_MAC='aa:aa:aa:55:55:55'
TNT2VNO1_CLIENT_MAC='aa:aa:aa:66:66:66'
TNT2VNO1_SERVER_MAC='aa:aa:aa:88:88:88'
#SFF1_MAC='aa:aa:aa:33:33:33'
#SFF2_MAC='aa:aa:aa:44:44:44'
#H1_MAC='00:00:00:11:11:11'
#H2_MAC='00:00:00:22:22:22'

def setStaticArp():

    os.system( "ssh fla@fla-server1 sudo arp -s %s %s -i eth1" %(FLA_SERVER3_IP,FLA_SERVER3_MAC) )
    os.system( "ssh fla@fla-server1 sudo arp -s %s %s -i eth1" %(FLA_SERVER3_IP2,FLA_SERVER3_MAC) )


    os.system( "ssh fla@fla-server3 sudo arp -s  %s %s -i eth1" %(FLA_SERVER1_IP, FLA_SERVER1_MAC) )
    os.system( "ssh fla@fla-server3 sudo arp -s  %s %s -i eth1" %(FLA_SERVER1_IP2, FLA_SERVER1_MAC) )

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
