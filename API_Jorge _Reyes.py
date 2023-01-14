#Librerias
from netmiko import ConnectHandler

Buscar_Mac = input("Mac: ")
Buscar_Mac = Buscar_Mac.replace("-","")
Buscar_Mac = Buscar_Mac.lower()

switch = input("IP: ")
user_user = input("Usuario: ")
user_pass = input("Contraseña: ")
enable_pass = input("Contraseña modo privilegiado: ")      


Device = {
    "host": switch,
    "username": user_user,
    "password": user_pass,
    "device_type": "cisco_ios",
    "secret": enable_pass,}

Connect_Device = ConnectHandler(**Device)             
Connect_Device.enable()                               

while True:
    try:
        
        
        cdp = Connect_Device.send_command("sh cdp neighbors detail",use_textfsm = True)

        for sw  in range(len(cdp)):
            Vecinos_P = (cdp[sw]["local_port"])
            Vecinos_P=list(Vecinos_P)

            try:
                dellist=("s","t","E","t","h","e","r","n","e","t")
                try:
                    for letra in dellist:
                        Vecinos_P.remove(letra)
                except: pass

            except:
                dellist=("i","g","a","b","i","t","E","t","h","e","r","n","e","t")
                try:
                    for letra in dellist:
                        Vecinos_P.remove(letra)
                except: pass

            Vecinos_P="".join(Vecinos_P)
            (cdp[sw]["local_port"])=Vecinos_P

    except:
        print("Error - busqueda cdp")
        pass

    try:
        mac_table = Connect_Device.send_command("show mac address-table",use_textfsm = True)

        for mac in range(len(mac_table)) :
            mac_a = (mac_table[mac]['destination_address'])

            mac_a = str(mac_a).replace(".","")
            mac_a = mac_a.lower()
            mac_table[mac]["destination_address"] = mac_a

    except:
        pass

    try: 
        for mac in range(len(mac_table)):

            print(mac_table[mac]['destination_address'])
            if Buscar_Mac == (mac_table[mac]['destination_address']):

                puerto = (mac_table[mac]['destination_port'][0])
            
            else:
                pass
        
        for mac in range(len(cdp)):
            puerto_t= (cdp[mac]["local_port"])
            ip_ssh=(cdp[mac]["management_ip"])

            try:

                if puerto == puerto_t:
                    Device = {
                        "host": ip_ssh,
                        "username": user_user,
                        "password": user_pass,
                        "device_type": "cisco_ios",
                        "secret": enable_pass,}
                        
                    Connect_Device = ConnectHandler(**Device)             
                    Connect_Device.enable()

                else:
                    output_run = Connect_Device.send_command("show run | include hostname")
                        
                    print('Mac',Buscar_Mac,'Conectado al puerto: ',puerto,'Switch',output_run)
                    Connect_Device.disconnect()
                    break

            except:
                print("La mac no existe")
                Connect_Device.disconnect()
                break
    except:
        pass