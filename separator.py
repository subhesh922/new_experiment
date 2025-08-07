import re 
for i in unique_part_category:
    if (i).upper().__contains__("HOUS"):
        print(i)





HOUSING
HOUSING + TP + DISPLAY
REAR HOUSING
HOUSING + TP
HANDLE/LOWER HOUSING
HOUSING - MIDDLE FRAME
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
Cell In[12], line 3
      1 import re 
      2 for i in unique_part_category:
----> 3     if (i).upper().__contains__("HOUS"):
      4         print(i)

AttributeError: 'float' object has no attribute 'upper'
