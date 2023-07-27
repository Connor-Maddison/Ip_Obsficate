import binascii, datetime, random, re, yaml

class Ip_Obsficate():

    def __init__(SELF, Input_File, Save_Loc, Operation):
        SELF.INPUT_FILE = Input_File
        SELF.SAVE_LOC = Save_Loc
        SELF.DECOYS = SELF.Load_Decoys()

        if (Operation == 0):
            ## Obsficate
            SELF.Init_Header()
            SELF.Obsficate_File()

        elif (Operation == 1):
            ##Deobsficate
            SELF.Init_Deobsfication_File()
            SELF.Deobsficate_File()

        else:
            print("ERROR")
            quit()

        

    ########################################################################
    # Conversion

    def Unicode_To_Dec(SELF, Input):
        if (type(Input) != bytes):
            Input = Input.encode('utf-8')
        
        return list(Input)

    def Dec_To_Unicode(SELF, Input):

        uni_bytes = ""
        ## convert to string but ensure hex format is maintained
        for dec in Input:
            if (type(dec) != int):
                dec = int(dec)

            conv_hex = hex(dec)[2:]
            if (len(conv_hex) <= 1):
                conv_hex = '0' + conv_hex
            uni_bytes += conv_hex
        
        return binascii.unhexlify(uni_bytes)


    ########################################################################
    # Writers


    def Init_Header(SELF):
        with open(f"{SELF.SAVE_LOC}/Interesting_IPs.md", "w") as file:
            file.write(f"# Interesting IPs \n## Last Updated: {datetime.datetime.now().strftime('%d-%m-%Y')}\n---\n ")

    def Obsficate_Writer(SELF, Content):
        with open(f"{SELF.SAVE_LOC}/Interesting_IPs.md", "a") as file:
            file.write(Content)



    def Init_Deobsfication_File(SELF):
        with open(f"{SELF.SAVE_LOC}/Notes.txt", "w") as file:
            file.write(f"\n")

    def Deobsficate_Writer(SELF, Content):
        with open(f"{SELF.SAVE_LOC}/Notes.txt", "ab") as file:
            file.write(Content)


    ########################################################################
    # Operations


    def Obsficate_File(SELF):
        with open(f"{SELF.INPUT_FILE}", "rb") as file:
            while True:

                buffer = file.read(1024)  

                if not buffer:
                    break

                SELF.IPv4_Translate(buffer)

    def Deobsficate_File(SELF):
        with open(f"{SELF.INPUT_FILE}", "r") as file:
            while True:

                buffer = file.read(1024)  

                if not buffer:
                    break

                SELF.Extract_IPv4(buffer)

    
    ########################################################################
    # Translations

    def IPv4_Translate(SELF, Buffer):
        byte_array = SELF.Unicode_To_Dec(Buffer)

        ips = ""
        while len(byte_array) > 0:
            group = []
            while len(group) < 4:
                if len(byte_array) > 0:
                    group.append(byte_array.pop(0))
                else:
                    group.append(0)

            mark = " "
            check_chance = random.randint(0,100)
            if check_chance < 6:
                ## 6% chance
                mark = "x"

            ips += f"- [{mark}] {group[0]}.{group[1]}.{group[2]}.{group[3]}\n"

            comment_chance = random.randint(0,100)
            if comment_chance < 4: 
                ## 4% chance   
                ips += SELF.Comment_Decoy()         

            group.clear
        
        print("Adding")
        SELF.Obsficate_Writer(ips)
        
    
    def Extract_IPv4(SELF, Buffer):
        
        ips = re.findall("[0-2]?[0-9]?[0-9]\.[0-2]?[0-9]?[0-9]\.[0-2]?[0-9]?[0-9]\.[0-2]?[0-9]?[0-9]", Buffer)
        ip_string = []
        for ip in ips: 
            split_ip = re.split("\.", ip)
            ip_string += split_ip
        
        SELF.Deobsficate_Writer(SELF.Dec_To_Unicode(ip_string))
        

    ########################################################################
    # Decoys

    def Load_Decoys(SELF):
        with open("./decoys.yaml", "r") as yaml_file:
            content = yaml.safe_load(yaml_file)
        return content

    def Comment_Decoy(SELF):
        
        random_alert = SELF.DECOYS["Alert"][random.randint(0,len(SELF.DECOYS["Alert"])-1)]
        random_intro = SELF.DECOYS["Intro"][random.randint(0,len(SELF.DECOYS["Intro"])-1)]
        random_action = SELF.DECOYS["Action"][random.randint(0,len(SELF.DECOYS["Action"])-1)]

        decoy_comment = f"---\n> {random_alert}{random_intro}{random_action}\n---\n"
        return decoy_comment


 
   




Ip_Obsficate("/home/kali/Downloads/hello.py", "/home/kali/Downloads/", 0)

#Ip_Obsficate("/home/kali/Downloads/Interesting_IPs.md", "/home/kali/Downloads/", 1)




