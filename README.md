# image-audit
Recursively scans a directory and compares crc's of images in a Minetest mod, 
game or texture pack to find duplicates, and possible copyright infringing 
images from Minecraft.

Compares crc's from images across all 8 Minecraft Java Edition resource pack
formats. The highest Minecraft release using each format was used to generate 
the crc list, namely:

Format 1 JE 1.8.9
Format 2 JE	1.10.2
Format 3 JE 1.12.2
Format 4 JE 1.14.4
Format 5 JE	1.16.1
Format 6 JE 1.16.5
Format 7 JE 1.17.1
Format 8 JE 1.18.2

Currently only png files are checked, and are only checked via crc so images 
that have been optimized for size will not be detected as originating from 
Minecraft. 

## usage
`$ python audit.py -i directory`
