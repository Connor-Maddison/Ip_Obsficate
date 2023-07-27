# ip_obsficate
Obsficate your content in the format of an unusual IP list security report markdown file. The produced report file is styled as a list of Ip's in a checklist form with randomly generated occasional comments to look like an engineers investigation notes. 

You can also add any extra text you desire as long as it is not in the format of an IP.

## Inputs:
Example Input: ***Ip_Obsficate("/home/kali/Project_Folder/hello.py", "/home/kali/Project_Folder/", [0 | 1])***

* Input_File : This is the file to be **Obsficated** or **Deobsficated** 
* Save_Loc : This is the location to save the **Obsficated Markdown File** ***(Interesting_IPs.md)*** or the **Deobsficated text File** ***(Notes.txt)***
* Operation:
    * 0 : Obsficate the Input_File
    * 1 : Deobsficate the Input_File