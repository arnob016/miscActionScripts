
One day I just think why we click done button every day why I don't this auto click then I create this script for skip boring clicks.



#### Click all done button of your current semester enrollment courses
```
python3 fast_exp.py -u <USERNAME_BLC> -p <PASSWORD_BLC> --mark
```

#### Click all done button of your target courses 
```
python3 fast_exp.py -u <USERNAME_BLC> -p <PASSWORD_BLC> --mark -c https://elearn.daffodilvarsity.edu.bd/course/view.php?id=14226 https://elearn.daffodilvarsity.edu.bd/course/view.php?id=14314
```

#### Click all done button of pecifice semester
```
python3 fast_exp.py -u <USERNAME_BLC> -p <PASSWORD_BLC> --mark --semi Spring22
```

#### Login with MoodleSession Cookes
```
python3 fast_exp.py --mark -m mjpdjq45us00egbmq7euqoo1bn
```

#### Upload file to Blc VPL
```
python3 fast_exp.py -m mjpdjq45us00egbmq7euqoo1bn -pfid 845720 -pf ./main.c 
```
pfid you can find on url of vpl page in id argument
https://elearn.daffodilvarsity.edu.bd/mod/vpl/forms/edit.php?id=845720&userid=33086


#### Explore all options
``` 
usage: fast_exp.py [-h] [-m M] [-pf PF] [-pfid PFID] [-c [C ...]] [-n] [-u U] [-p P] [-t]
                   [--mark | --no-mark] [--all | --no-all] [--semi SEMI]

Auto geting blc exp. Just for fun!

options:
  -h, --help         show this help message and exit
  -m M               Your MoodleSession cookies!
  -pf PF             Which file you want to post
  -pfid PFID         Here is your post id ex: edit.php?id=844835
  -c [C ...]         Your target courses links!
  -n                 Hide your name!
  -u U               Username
  -p P               Password
  -t                 Run in Thread
  --mark, --no-mark  Click all mark as completed
  --all, --no-all    Work with all courses, without this flag auto get latest semister
  --semi SEMI        Define which semister with working ex: --semi Fall21
  ```
  
  
