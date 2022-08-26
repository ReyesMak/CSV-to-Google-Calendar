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
1. Start Date/ End Date: MM/DD/YY e.g. *01/01/22*
2. Start Time/ End Time: 24-hour format e.g. *14:00* ✅ *2:00p.m* ❌ *09:00* ✅ *9:00a.m* ❌
3. All Day Event: Boolean value e.g. *TRUE*/*FALSE*
4. Description: Optional
5. Location: Optional
6. Guests: emailA,emailB,emailC e.g. *abc@gmail.com,def@gmail.com* ✅ *abc@gmail.com, def@gmail.com* (extra space) ❌ *[abc@gmail.com, def@gmail.com]* (list format) ❌

___________________________________________________________________________________________________________________________________________________________

The Google Account used in this code is defaultly set as admin@preface.education. To change the Google account, the ```client_secret.json``` needs to be updated.

Getting your client_secret.json file, you can do that by signing into the Google Cloud Platform:
https://console.cloud.google.com/

___________________________________________________________________________________________________________________________________________________________

To import the data of csv file into a specofic calendar, first you need the **calendarId** which can be accessed by Google Calendar.

For example, in order to import the schedule into the [CWB] Summer 22 Boot Camp, you can retrieve the calendarId by doing so

Go to the specific calendar and select **Settings and sharing**:

<img width="1405" alt="image" src="https://user-images.githubusercontent.com/108719212/186839716-c167cda3-2ce1-472e-bbb3-f11cc7eac671.png">

Scroll down and copy the calendarId:

<img width="800" alt="image" src="https://user-images.githubusercontent.com/108719212/186839947-62ec5627-f04b-45e4-a485-de2a69ecb069.png">

After coping the calendarId, paste it onto line 86 of the ```csv_to_GoogleCalendar.py```:

```id = "preface.education_9me0qsqf7qepo2gq6tama7ujls@group.calendar.google ```
___________________________________________________________________________________________________________________________________________________________

Therefore, you run the code and the import of schedule from csv file to Google Calendar should be successful!!!

Remarks:

The dictionary printed out with the format of {{Course Name} : string} shows the random requestId generated for the Google Calendar API.


