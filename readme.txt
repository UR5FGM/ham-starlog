            Ham-star Log version 2.0.
            Author: Serhii Kolomiitsev <serge.kolomeitsev@gmail.com>.

        System requirements:
        Windows 7 and higher, Linux or any OS with Python 3.8 or higher.

        Files:
        divs.csv – divisions list of CB callsigns;
        ham-starlog.exe - executable  file to run under Windows;
        ham-starlog.pyc – source file to run in Python;
        prefix_list.csv – list of amateur radio callsign prefixes.
        folder "manual" contains the manual in English and Ukrainian.

    Ham-star Log is a radio amateur log designed to record radio amateur contacts. Unlike other logs, it operates in terminal mode, which ensures maximum efficiency. Keyboard control is carried out using simple commands and parameters. Enjoy comfortable communication on the air using only keyboard, instead of searching for tabs and buttons in graphical interface. The screen displays only information you need at the moment.

    Run ham-starlog.exe, or ham-starlog.pyc if Python is installed. You're prompted to enter a profile name. If you don't  have a profile yet, enter desired name and, agree to create a new profile, type "Y" and press Enter.
You will be prompted to select a profile type.
1 (HAM) - amateur radio profile;
2 – CB profile;
3 (SWL) – Shortwave listener profile.
Type the number according your choice, then press enter.
Enter your name and callsign. The application is ready to work after greeting. Your profile will be placed in folder "profiles". It contains a log file, configuration file and folders: "backup", "export" and "import". Use this profile name the next time you run the application. Running the application with a  different name will create a new profile. You can create any number of profiles with different settings.

    First, type the command "qso" and press "Enter". Then type callsign of the operator you are communicating with. Information about the number of connections with this operator, his country, CQ-zone and ITU-zone is displayed.
Enter a signal report that you are sending. If you leave the field "Report sent" empty, the default report is   "595" for AM and FM, "599" for CW, and "59" for other modulations.
In the next field "Report RCVD" Enter the signal report you received. If you leave this field empty, the default report is "595" for AM and FM, "599" for CW, and "59" for other modes.
Enter the operator's name. If you leave this field blank, to the log is added "Name: UNKNOWN". This field will appear every time you contact this operator until it's filled in. Otherwise, the name will be determined automatically when you contact him again.
Enter the location (QTH). If you leave this field empty, to the log is added "QTH: UNKNOWN". The field "QTH" will appear each time you contact again until it's filled.
In the field Gridsquare, enter the operator's QTH Locator. This field is optional.
You shouldn't care about uppercase and lowercase letters. The application inserts it automatically. This ensures the best performance and convenience.
The field "Band/frequency" is required. Type your operating band or frequency in kHz. For example: if you enter "160", to the log will be added " 160 M". If you enter a frequency, in kHz, band will be determined automatically.
The field "Mode" is required. You can enter modulation type manually or using keystrokes. Enter a number from 1 to 6. The following values are available:
1 – USB, 2 – LSB, 3 – CW, 4 – AM, 5 – FM, 6 – DIGI.
Write a short comment (200 characters) in the field "Comment". It could contain information about an equipment, phone number, email, etc. The last comment will be displayed each time you connect to this operator again. You can view all comments using command "info" with the callsign. However, you can leave the field "comment" empty.
Message "Success" means that the reccord was successfully added to the log. Congratulations! You've made your first QSO.

    The command "qso" can be also entered with a callsign. For example:
"qso ok2xxx". In this case, the field "callsign" is not displayed.
    You can interrupt record at any time by entering command "skip" in any field.
    Enter "INFO" and a callsign to get information about an operator. Enter "INFO and the operator's callsign" you just contacted, or "info log" to get log information.
For example:

Enter command: info ok2xxx
0 QSO. Czech Republic. CQ-zone: 15, ITU-zone: 28.

After contact:

Enter command: info ok2xxx
1 QSO. Name: Pavel. QTH: Prague Czech Republic.
CQ-zone: 15, ITU-zone: 28.
1- NOV 11 2024, 20:43:10. TX: 599, RX: 599. Band: 160M, CW.
Comment: "my first contact."

Enter command: info log
Log contains 1 record, 1 callsign and 1 country.

So, command "INFO callsign" shows all available information about the operator;; command "info log" shows the number of connections, number of unique callsigns, and number of territories in this log. This command should always used with a callsign, or with parameter "log".

    However, your work can be even more comfortable. If you're going to use one frequency or band for a long time, you can set it with command "band".
For example:

Enter command: band 160
Band set to 160M (1810 - 2000 kHz).

Enter command: band 1850
Band set to 160M (1850 kHz).

After that, the band or frequency is recorded automatically and the field "band" is not displayed during next contacts. Use this command whenever you change the band or frequency. Instead of the command "band", you can use command "freq" .
    The command "mode" sets modulation type. Use this command whenever you're going to work with the same modulation for a long time.
For example:

Enter command: mode cw
Mode set to CW.

You can also set the modulation type using keystrokes. For example:

Enter command: mode 3
Mode set to CW.

Use this command whenever you want to change modulation.
    If you are on an expedition or participating in a contest, , sometimes you need to assign a progressive number to each QSO. To enable this, use command "numbers". Enter this  command again to turn this feature off. 
To set start of a count, use command "counter" with a number. For example:

Enter command: counter 500
Progressive numbers set from 500.

By default, the count starts from "001".
    The command "time" displays the current time UTC and duration of the current session. For example:

Enter command: time
13:00 UTC. Duration of the current session: 0:20:43.

    The command "contacts" shows the number of contacts, number of unique callsigns, and number of countries. This command should be used with parameter "all" or "last". Parameter "all" shows the number of contacts in the log. Parameter "last" shows the number of contacts you've made during current session time.
    The command "export" exports the log to TXT and ADIF formats. Use this command with the "all" or "last" parameter. Parameter "all" exports all contacts. Parameter "last" exports only contacts from the current session.
The exported files are in folder "export".
    The command "import" imports data from an "ADIF" file that created by another application or downloaded from Hamlog. Attention! Place the "*.adi" file to folder "import" and rename it "log.adi" then enter command "import". After that, the data from file "log.adi" will be imported into the log. A previous copy of the log will be saved in folder "backup".
    To clear the display, use command "clear".
    The command "help" shows a short manual.
    The command "commands" shows a list of commands.
    To exit the application, use command "Stop" or "exit".

    List of all commands:
-BAND: sett band or frequency;
-CLEAR: clear the display;
-CONTACTS (all, last): show the number of records and callsigns;
-COMMANDS: display the list of commands;
-COUNTER (number): set the initial progressive TX counter number;
-EXIT: exit the application;
-EXPORT (last, all): export log;
-FREQ: set band or frequency;
-HELP: show help;
-IMPORT: Import data from the file "log.adi";
-INFO (call, log): display all records with the operator, show log information;
-MODE (modulation): set modulation;
-NUMBERS: enable/disable progressive numbers;
-QSO (callsign): create a new record;
-SKIP: interrupt recording;
-STOP: exit the program;
-TIME: displays UTC time and duration of the current session.

    If you have the opportunity, please support me via Paypal:
serge.kolomeitsev@gmail.com
Please contact me if you have any suggestions or comments.
    Enjoy your time on the air.
          Best 73,

