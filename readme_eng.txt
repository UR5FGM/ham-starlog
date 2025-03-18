          Ham-star Log version 1.0.
Author: Serhii Kolomiitsev <serge.kolomeitsev@gmail.com>.
System requirements:
Windows 7 or higher 32-bit or 64-bit, Linux or other operating systems with installed Python 3.8 or higher.
Files:
divs.csv - list of divisions of CB callsigns;
ham-starlog.exe - executable file to run under Windows;
ham-starlog.pyc - source file to run in the Python interpreter;
prefix_list.csv - list of amateur radio callsign prefixes.

    Ham-star Log is an amateur radio log that's intended for recording radio communications. Unlike other logs, it runs in terminal mode, which ensures maximum efficiency. Keyboard control is carried out with simple commands and parameters. 
Enjoy comfortable on-air communication using only your keyboard, instead of searching for tabs and buttons in the graphical interface. The screen only displays information that is needed at the moment.

    Run the ham-starlog.exe file. You will be prompted to enter a profile name. if you don't have a profile yet, enter the name you wish and agree to create a new profile, type "Y" and press enter.
You will be prompted to select a profile type.

1 (HAM) - amateur radio profile;
2 - CB profile;
3 (SWL) - radio listener profile. 
Type the number according your choice, then press enter.
    Enter your name and call sign. After the greeting, the log is ready to work. Your profile will appear in the "profiles" folder. It contains a log file, a configuration file and "export" folder. Use this profile name the next time you start the log. Starting the program with a different name will create a new profile. You can create any number of profiles with different parameters.

    First, type the command "qso" and press "Enter". Then type callsign of the operator you are communicating with. Information about the number of QSOs with this operator, his country, CQ-zone and ITU-zone will appear. 
    Type signal report that you are sending him. If you leave the field "Report TX" blank, in the log will be writen "595" for AM and FM, "599" for CW, and "59" for other modes.
    Type the signal report you received. If you leave it blank, the default report will be "595" for AM and  FM, "599" for CW, and "59" for other modes.
    Type the name of the operator you are contacting. If you leave this field blank, the word "UNKNOWN" will be added to the log.
The field "Name" will appear every time you contact this operator. Otherwise,   the name will be added automatically when you contact him again.
    Type the location or QTH locator. If you leave this field blank, the word "UNKNOWN" will be added to the log. The field "QTH" will appear every time you contact him again until it's filled in.
Otherwise, QTH will be added automatically when you contact this operator again.
    Don't worry about upper and lower case letters. The program will insert it automatically. It ensures the best performance and convenience.
    The field "Band / Frequency" is required. Type your operating band or frequency.
For example. If you type "160", to the log will be added "160 m". If you type "CB", to the log will be  added "CB band".
    The field "Mode" is required. You can enter modulation type manually, or use keystrokes. Enter a number from 1 to 6.
The following values ​​are available:
1 - USB, 2 - LSB, 3 - CW, 4 - AM, 5 - FM, 6 - DIGI.
    Write a short comment (200 characters in the field "Comment. It coult contain information about an equipment, a phone number, e-mail, etc. The last comment will be shown each time you connect with this operator again. You can see all comments using command "info callsign". However, you can leave the "Comment" field empty. 
    Message "Success" means that the reccord was successfully added to the log. Congratulations! You've made your first QSO.
    You can also use the command "qso" with a "callsign". For example:
"qso ok2xxx".
In this case, the field "callsign" will not appear.
    You can abort record at any time by typing command "skip" in any field.
    Type "INFO" and callsign to get information about an operator. Type "INFO callsign" of the operator you just contacted.
For example:

Enter command: info ok2xxx
0 QSO. Czech Republic. CQ-zone: 15, ITU-zone: 28.

After contact:
Enter command: info ok2xxx
1 QSO. Name: Pavel. QTH: Prague Czech Republic.
CQ-zone: 15, ITU-zone: 28.
1- NOV 11 2024, 20:43:10. RTX: 599, RRX: 599. Band: 160 m. CW.
Comment: "my first contact."

     So, command "INFO callsign" shows all information that's currently available.You must always use this command with "callsign".
    However, your work can be even more comfortable. If you're going to use one frequency or band for a long time, you could set it with  the command "band". For example:
Enter command: band 160
Band set to 160 m.

After that, band or frequency will be recorded automatically and the field "band" will not appear during the QSO. Use this command every time you change band or frequency.
    The command "mode" sets the modulation type. Use this command every time you're going to work with one mode for a long time.
For example:
Enter command: mode cw
Mode set to CW.

Also, you could set modulation type using keystrokes. For example:
Enter command: mode 3
Mode set to CW.

Use this command every time you want to change modulation.
    If you are on an expedition or participating in a contest, sometimes you need to assign a progressive number to each QSO. use command "numbers" to turn this on. Type this command again to turn this feature off. 
To set the starting point, use command "counter" with a number. For example:
Enter command: counter 500
Progressive numbers set from 500.

By default, the countdown starts from "001".
    The command "time" displays current time UTC and duration of the current session. For example:
Enter command: time
13:00 UTC. Duration of the current session: 0:20:43.

    The command "contacts" shows the number of contacts, number of unique callsigns and countries in the log. You should always use this command with parameter "all" or "last". Parameter "all" shows the number of contacts in the log. Parameter "last" shows the number of contacts you make during the current session.
    The command "export" exports the log into a text file. Use this command with parameter "all" or "last". Parameter "all" exports contacts from the log. Parameter "last" exports contacts from the current session. You can find TXT files in the folder "export".
    Use the command "clear" to clear the display.
    The command "help" shows a short manual.
    The command "commands" shows the commands list.
    Use command "Stop" to exit the program.

    List of all commands:
-BAND (band / frequency): set band;
-CLEAR: clear display;
-CONTACTS (all, last): show number of records and callsigns;
-COMMANDS - display commands list;
-COUNTER (number): set initial progressive number TX of the counter;
-EXPORT (all, last): export log into text format;
-HELP: display help;
-INFO (callsign): display all records with this operator;
-MODE (mode) - set mode;
-NUMBERS: turn on / off progressive numbers;
-QSO (callsign): create a new record;
-SKIP: skip contact;
-STOP: exit programm;
-TIME: display UTC time and duration of the current session.

    If you have an opportunity, please support me via Paypal: serge.kolomeitsev@gmail.com
Please contact me if you have any suggestions or comments.
Enjoy your time on air.
          Best 73,
          Serhii Kolomiitsev