# CSV-to-Google-Calendar

Before executing the code, users need to ensure that they have installed the required libraries in the conda env (optional):
1. pandas : ``` pip install pandas ```
2. Google client : ```  pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib```
3. string : ``` pip install strings```


I strongly recommend using **Visual Studio Code** as the IDE for running the code.
Nevertheless, the code would still work with PyCharm or other IDE.

Here is the link of installing **Visual Studio Code** : https://code.visualstudio.com/download

___________________________________________________________________________________________________________________________________________________________

For the csv file, the file name ***MUST*** be ```csv_file.csv``` and it has to be put in the same folder consisting of both the 
```client_secret.json``` and ```csv_to_GoogleCalendar.py```.

The format in the csv file must follow the following rule:
1. Start Date/ End Date: MM/DD/YY
2. Start Time/ End Time: 14:00✅ 2:00p.m.❌ 09:00✅ 9:00a.m.❌
3. All Day Event: TRUE/FALSE (Boolean value)
4. Description: Optional
5. Location: Optional
6. Guests: kelvin.chan@preface.education,reyes.mak@preface.education✅ kelvin.chan@preface.education, reyes.mak@preface.education (extra space)❌ [kelvin.chan@preface.education, reyes.mak@preface.education]❌

___________________________________________________________________________________________________________________________________________________________




