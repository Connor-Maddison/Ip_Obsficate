##########################
# IP_OBSFICATOR
# Created by: Connor-Maddison
# Creation Date: 27/07/2023
# Last Updated: 27/07/2023
##########################


import re, logging
from yaml import safe_load
from random import randint
from datetime import datetime
from binascii import unhexlify
from pathlib import Path


########################################################################
# Logging Setup

class ColourFormatter(logging.Formatter):
    cyan = "\x1b[96m"
    yellow = "\x1b[33m"
    red = "\x1b[31m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(levelname)s - %(message)s "

    FORMATS = {
        logging.DEBUG: "%(asctime)s - " + cyan + format + reset,
        logging.INFO: "%(asctime)s - " + cyan + format + reset,
        logging.WARNING: "%(asctime)s - " + yellow + format + reset,
        logging.ERROR: red + "%(asctime)s - " + format + reset,
        logging.CRITICAL: bold_red + "%(asctime)s - " + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger()
logger.setLevel(logging.WARNING)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(ColourFormatter())
logger.addHandler(consoleHandler)





########################################################################
# Obsfication Code


class Ip_Obsficate():

    def __init__(SELF, Operation):
        SELF.INPUT_FILE = None
        SELF.SAVE_LOC = "./"
        SELF.OP = Operation
        
        

    def Trigger_Start(SELF):

        if (SELF.INPUT_FILE is None) or (SELF.SAVE_LOC is None):
            logger.error(f"Missing Valid target and/or save locations")
            quit()

        if (SELF.OP == 0):
            ## Obsficate
            SELF.DECOYS = SELF.Load_Decoys()
            logger.info(f"Obsficating {SELF.INPUT_FILE}")
            SELF.Init_Header()
            SELF.Obsficate_File()

        elif (SELF.OP == 1):
            ##Deobsficate
            logger.info(f"Deobsficating {SELF.INPUT_FILE}")
            SELF.Init_Deobsfication_File()
            SELF.Deobsficate_File()

        else:
            logger.error(f"No Operation Selected, Please select option [0] - Obsficate, [1] - Deobsficate")
            quit()

    ########################################################################
    # Conversion

    def Unicode_To_Dec(SELF, Input):
        logger.info(f"Converting Unicode to Decimal")
        if (type(Input) != bytes):
            logger.warning(f"Non byte input input into Unicode_To_Dec")
            Input = Input.encode('utf-8')
        
        return list(Input)

    def Dec_To_Unicode(SELF, Input):

        logger.info(f"Converting Decimal to Unicode")
        uni_bytes = ""
        ## convert to string but ensure hex format is maintained
        for dec in Input:
            if (type(dec) != int):
                dec = int(dec)

            if (dec == 0):
                logger.debug(f"Removing Null bytes")
                continue

            conv_hex = hex(dec)[2:]
            if (len(conv_hex) <= 1):
                conv_hex = '0' + conv_hex
            uni_bytes += conv_hex
        
        return unhexlify(uni_bytes)


    ########################################################################
    # Writers


    def Init_Header(SELF):
        logger.info(f"Initialising Interesting_IPs.md file")
        with open(f"{SELF.SAVE_LOC}/Interesting_IPs.md", "w") as file:
            file.write(f"# Interesting IPs \n## Last Updated: {datetime.now().strftime('%d-%m-%Y')}\n---\n ")

    def Obsficate_Writer(SELF, Content):
        logger.info(f"Writing to {SELF.SAVE_LOC}/Interesting_IPs.md file")
        with open(f"{SELF.SAVE_LOC}/Interesting_IPs.md", "a") as file:
            file.write(Content)



    def Init_Deobsfication_File(SELF):
        logger.info(f"Creating Conversion file (Notes.txt)")
        with open(f"{SELF.SAVE_LOC}/Notes.txt", "w") as file:
            file.write(f"\n")

    def Deobsficate_Writer(SELF, Content):
        logger.info(f"Writing to Conversion file ({SELF.SAVE_LOC}/Notes.txt)")
        with open(f"{SELF.SAVE_LOC}/Notes.txt", "ab") as file:
            file.write(Content)


    ########################################################################
    # Operations


    def Obsficate_File(SELF):
        logger.info(f"Reading target file")
        with open(f"{SELF.INPUT_FILE}", "rb") as file:
            buffer = file.read()  

            SELF.IPv4_Translate(buffer)

    def Deobsficate_File(SELF):
        logger.info(f"Reading target file")
        with open(f"{SELF.INPUT_FILE}", "r") as file:
            buffer = file.read()  
            
            SELF.Extract_IPv4(buffer)

    
    ########################################################################
    # Translations

    def IPv4_Translate(SELF, Buffer):
        logger.info(f"Translating to IPv4 format")
        byte_array = SELF.Unicode_To_Dec(Buffer)

        ips = ""
        while len(byte_array) > 0:
            group = []
            while len(group) < 4:
                if len(byte_array) > 0:
                    group.append(byte_array.pop(0))
                else:
                    group.append(0)

            logger.debug(f"Created IP: {group}")
            mark = " "
            check_chance = randint(0,100)
            if check_chance < 6:
                ## 6% chance
                mark = "x"

            ips += f"- [{mark}] {group[0]}.{group[1]}.{group[2]}.{group[3]}\n"

            comment_chance = randint(0,100)
            if comment_chance < 4: 
                ## 4% chance 
                ips += SELF.Comment_Decoy()         

            group.clear
        
        SELF.Obsficate_Writer(ips)
        
    
    def Extract_IPv4(SELF, Buffer):
        
        logger.info(f"Extracting IPs from target file")

        ips = re.findall("[0-2]?[0-9]?[0-9]\.[0-2]?[0-9]?[0-9]\.[0-2]?[0-9]?[0-9]\.[0-2]?[0-9]?[0-9]", Buffer)
    
        ip_string = []
        for ip in ips: 
            logger.debug(f"Found IP {ip}")
            split_ip = re.split("\.", ip)
            ip_string += split_ip
        
        SELF.Deobsficate_Writer(SELF.Dec_To_Unicode(ip_string))
        

    ########################################################################
    # Decoys

    def Load_Decoys(SELF):
        logger.debug(f"Located decoys.yaml file")
        path = Path(__file__).parent / "./decoys.yaml"
        with open(path, "r") as yaml_file:
            content = safe_load(yaml_file)
        
        logger.info(f"Created decoys selection")
        return content

    def Comment_Decoy(SELF):
        
        random_alert = SELF.DECOYS["Alert"][randint(0,len(SELF.DECOYS["Alert"])-1)]
        random_intro = SELF.DECOYS["Intro"][randint(0,len(SELF.DECOYS["Intro"])-1)]
        random_action = SELF.DECOYS["Action"][randint(0,len(SELF.DECOYS["Action"])-1)]

        decoy_comment = f"---\n> {random_alert}{random_intro}{random_action}\n---\n"
        logger.debug(f"Created a Decoy comment : {decoy_comment}")
        return decoy_comment


 
   



########################################################################
# CLI interface

from sys import argv
from os.path import isdir, isfile



class CLI_Controls():
    def __init__(SELF, args):
        SELF.ARGS = args
        
        ## Switch between deobsfication and obsfication
        switch = 0

        ## parse first arg
        if (SELF.ARGS[0] == "-h"):
            logger.info("Displaying Help pannel")
            print(SELF.Help_Output())
            quit()
        elif (SELF.ARGS[0] == "0") or (SELF.ARGS[0] == "obsficate"):
            logger.info("Preping Obsfication tool")
            SELF.TOOL_CLASS = Ip_Obsficate(0)
        elif (SELF.ARGS[0] == "1") or (SELF.ARGS[0] == "deobsficate"):
            logger.info("Preping Deobsfication Tool")
            SELF.TOOL_CLASS = Ip_Obsficate(1)
        else:
            logger.error("Missing suitable operation option, use -h for help")
            quit()

        SELF.ARGS.pop(0)

        while len(SELF.ARGS) > 0:
            SELF.Handle()
        SELF.TOOL_CLASS.Trigger_Start()



    def Help_Output(SELF):
        display = """
----------------------------------------------
ip_obsficator
Created by: Connor-Maddison
----------------------------------------------

Example Use: 

    python3 ip_obsficator [OPTION] [ARGS]
    python3 ip_obsficator.py obsficate -i /PATH/TARGET_FILE.EXT -o /PATH 


ARGS:
----------------------------------------------
-h  : 
    : Shows this help page
-i  : <Path/File>
    : Target input file (enter relative or absolute path to file) 
-o  : <Path>
    : Output file path (enter relative or absolute path) <DEFAULT = Current Directory>
-v  : 
    : Print verbose output


OPTIONS:
----------------------------------------------
To select between either obsficate or deobsficate either use their fullname or [0 | 1]

obsficate | [0] : Obsficate the target file
deobsficate | [1] : Deobsficate the target file

----------------------------------------------

"""
        return display
    
    def Handle(SELF):
        
        arg = SELF.ARGS.pop(0)

        if (arg == "-i"):

            if len(SELF.ARGS) < 1:
                logger.error(f"{arg} Invalid argument passed no value added")
                quit()

            value = SELF.ARGS.pop(0)
            if isfile(value):
                logger.info(f"Added input file: {value}")
                SELF.TOOL_CLASS.INPUT_FILE = value
            else:
                logger.error(f"{value} is not a valid file")
                quit()


        elif (arg == "-o"):

            if len(SELF.ARGS) < 1:
                logger.error(f"{arg} Invalid argument passed no value added")
                quit()
            value = SELF.ARGS.pop(0)
            if isdir(value):
                logger.info(f"Added save loc: {value}")
                SELF.TOOL_CLASS.SAVE_LOC = value
            else:
                logger.error(f"{value} is not a valid directory")
                quit()

        elif (arg == "-v"):
            
            logger.setLevel(logging.INFO)
            logger.info(f"Using verbose logging")
        
        else :

            logger.warning(f"{arg} is not a valid argument")



args = argv[1:]
CLI_Controls(args)



