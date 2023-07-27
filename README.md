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

## Example report:

# Interesting IPs 
## Last Updated: 27-07-2023
---
- [x] 105.109.112.111
- [ ] 114.116.32.112
- [ ] 116.121.44.32
- [ ] 111.115.44.32
- [ ] 114.101.44.32
- [ ] 112.121.112.101
- [ ] 114.99.108.105
- [ ] 10.102.114.111
---
> Uncommon Geolocation: An IP address with reverse DNS discrepancies is attempting to access sensitive areas of your network. Verify its legitimacy immediately.
---
- [ ] 101.101.112.32
- [ ] 10.10.100.101
---
> Attention: These have been listed in our database as a known source of malware distribution. Investigate to ensure your security is not compromised.
---