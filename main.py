from datetime import datetime, timezone
import csv
import os


class New_contact:
    def __init__(
        self,
        callsign,
        report_tx,
        report_rx,
        name,
        qth,
        cq_zone,
        itu_zone,
        date,
        band,
        mode,
        prog_number_tx,
        prog_number_rx,
        comment,
    ):
        self.callsign = callsign
        self.report_tx = report_tx
        self.report_rx = report_rx
        self.name = name
        self.qth = qth
        self.cq_zone = cq_zone
        self.itu_zone = itu_zone
        self.date = date
        self.band = band
        self.mode = mode
        self.prog_number_tx = prog_number_tx
        self.prog_number_rx = prog_number_rx
        self.comment = comment


class Logreader:
    def __init__(self, prefix_list, profile_type):
        self.prefix_list = prefix_list
        self.profile_type = profile_type

    def country(self, callsign):
        country = ""
        digits = 0
        self.cq_zone = ""
        self.itu_zone = ""
        for char in callsign:
            if char.isdigit():
                digits += 1
        if digits == 0:
            callsign = ""
        for column in csv.DictReader(self.prefix_list, delimiter="|"):
            if column["Prefix"] in callsign[: len(column["Prefix"])]:
                country = column["Country"]
                self.cq_zone = column["CQ-zone"]
                self.itu_zone = column["ITU-zone"]
        prefix_list.seek(0)
        return country

    def _print_date(date):
        if len(date) == 0:
            return
        date = date.split()
        months = (
            "JAN",
            "FEB",
            "MAR",
            "APR",
            "MAY",
            "JUN",
            "JUL",
            "AUG",
            "SEP",
            "OCT",
            "NOV",
            "DEC",
        )
        time = date[1]
        date_new = date[0].split("-")
        year = date_new[0]
        month = int(date_new[1]) - 1
        month = months[month]
        if int(date_new[2]) < 10:
            day = date_new[2][1]
        else:
            day = date_new[2]
        return f"{month} {day} {year}, {time}"

    def search(self, log, callsign=""):
        qso_counter = 0
        all_contacts_counter = 0
        tx = ""
        rx = ""
        name = ""
        qth = ""
        cq_zone = ""
        itu_zone = ""
        date = ""
        last_date = ""
        band = ""
        mode = ""
        comment = ""
        last_comment = ""
        last_contact = ""
        info = ""
        callsigns = []
        countries = []
        self.last_contact = ""
        self.info = ""
        self.all_contacts_counter = 0
        self.callsigns = 0
        self.countries = 0
        self.name = ""
        self.qth = ""

        for column in csv.DictReader(log, dialect="excel"):
            if len(column["Callsign"]) > 0:
                all_contacts_counter += 1
            if column["Callsign"] not in callsigns:
                callsigns.append(column["Callsign"])
            if (
                column["QTH"].split(",")[-1] != " "
                and column["QTH"].split(",")[-1] not in countries
            ):
                countries.append(column["QTH"].split(",")[-1])
            if column["Callsign"] == callsign:
                qso_counter += 1
                tx = column["Report TX"]
                if self.profile_type == "3":
                    rx = ""
                else:
                    rx = column["Report RX"]
                self.name = column["Name"]
                if column["Name"] == "UNKNOWN":
                    name = ""
                else:
                    name = f'Name: {column["Name"]}.'
                self.qth = column["QTH"]
                qth = f'QTH: {column["QTH"]}.'
                if len(column["CQ-zone"]) > 0:
                    cq_zone = f'\nCQ-zone: {column["CQ-zone"]}, '
                else:
                    cq_zone = ""
                if len(column["ITU-zone"]) > 0:
                    itu_zone = f'ITU-zone: {column["ITU-zone"]}.'
                else:
                    itu_zone = ""
                date = column["Date"]
                band = column["Band / Frequency"]
                mode = column["Mode"]
                comment = column["Comments"]
                if comment != "":
                    last_comment = f"\n\tLast comment: {comment}"
                    comment = f"\tComment: {comment}\n"
                if self.profile_type == "3":
                    info += f"{qso_counter}- {Logreader._print_date(date)}. Report: {tx}. Band: {band} {mode}.\n{comment}"
                else:
                    info += f"{qso_counter}- {Logreader._print_date(date)}. RTX: {tx}, RRX: {rx}. Band: {band} {mode}.\n{comment}"
        last_date = Logreader._print_date(date)
        self.callsigns = len(callsigns)
        self.countries = len(countries)
        self.all_contacts_counter = all_contacts_counter
        if (
            len(qth) == 0
            and len(self.country(callsign)) > 0
            or "UNKNOWN" in self.qth
            and len(self.country(callsign)) > 0
        ):
            qth = f"{self.country(callsign)}."
        elif "UNKNOWN" in self.qth and len(self.country(callsign)) == 0:
            qth = ""
        self.info = f"\t{qso_counter} QSO. {name} {qth}{cq_zone}{itu_zone}\n{info}"
        if len(cq_zone) == 0 and len(self.country(callsign)) > 0:
            cq_zone = f"CQ-zone: {self.cq_zone}, "
        if len(itu_zone) == 0 and len(self.country(callsign)) > 0:
            itu_zone = f"ITU-zone: {self.itu_zone}."
        if qso_counter == 0:
            self.last_contact = f"\t{qso_counter} QSO. {qth} {cq_zone}{itu_zone}\n"
            self.info = f"\t{qso_counter} QSO. {qth} {cq_zone}{itu_zone}\n"
        else:
            self.last_contact = f"\t{qso_counter} QSO. {name} {qth}{cq_zone}{itu_zone}\nLast QSO: {last_date}. Band: {band}, {mode}.{last_comment}"


def help(commands_list):
    print(
        f"-{commands_list[0]} (band / frequency): set band;\n-{commands_list[1]}: clear display;\n-{commands_list[2]} (all, last): show number of records and callsigns;\n-{commands_list[3]} - display commands list;\n-{commands_list[4]} (number): set initial progressive number TX of the counter;\n-{commands_list[5]} (all, last): export log into text format;\n-{commands_list[6]}: display this help;\n-{commands_list[7]} (callsign): display all records with this operator;\n-{commands_list[8]} (mode) - set mode;\n-{commands_list[9]}: turn on / off progressive numbers;\n-{commands_list[10]} (callsign): create a new record;\n-{commands_list[11]}: skip contact;\n-{commands_list[12]}: exit programm;\n-{commands_list[13]}: display time UTC and duration the current session."
    )


def new_profile(profilename):
    username = ""
    user_callsign = ""
    profile_type = ""
    while True:
        profile_type = input("Select profile type: <1> - HAM, <2> - CB, <3> - SWL. ")[
            :1
        ]
        if profile_type == "1" or profile_type == "2" or profile_type == "3":
            break
        else:
            print("Incorrect profile type.")
    while True:
        username = input("Your name: ")[:20].title()
        if len(username) > 0 and username.isalpha():
            break
    if profile_type == "1" or profile_type == "2":
        while True:
            user_callsign = input("Your callsign: ")[:20].upper()
            if len(user_callsign) > 0:
                break
    if not os.path.isdir(f"profiles/{profilename}"):
        os.mkdir(f"profiles/{profilename}")
    config = open(f"profiles/{profilename}/{profilename}.ini", "w", encoding="UTF8")
    config.write(
        f"profilename={profilename}\nprofiletype={profile_type}\nname={username}\ncallsign={user_callsign}\nqth=\n"
    )
    config.close()
    if not os.path.isdir(f"profiles/{profilename}/export"):
        os.mkdir(f"profiles/{profilename}/export")
    log = open(
        f"profiles/{profilename}/{profilename}.csv", "w", encoding="UTF8", newline=""
    )
    logwriter = csv.writer(log, dialect="excel")
    if profile_type == "1" or profile_type == "2":
        logwriter.writerow(
            [
                "Callsign",
                "Report TX",
                "Report RX",
                "Name",
                "QTH",
                "CQ-zone",
                "ITU-zone",
                "Date",
                "Band / Frequency",
                "Mode",
                "Progressive number TX",
                "Progressive number RX",
                "Comments",
            ]
        )
    elif profile_type == "3":
        logwriter.writerow(
            [
                "Callsign",
                "Report TX",
                "Name",
                "QTH",
                "CQ-zone",
                "ITU-zone",
                "Date",
                "Band / Frequency",
                "Mode",
                "Comments",
            ]
        )
        log.close()


def read_config(config, profilename):
    params = {}
    for parameter in config:
        params[parameter.split("=")[0]] = parameter.split("=")[1].strip("\n")
        if params["profilename"] != profilename:
            print("invalid profile!")
            return
    return params


def export_last(log, profile_type):
    if not os.path.isdir(f"profiles/{profilename}/export"):
        os.mkdir(f"profiles/{profilename}/export")
    file = open(
        f'profiles/{profilename}/export/{datetime.now(timezone.utc).strftime("%Y-%m-%d")}.txt',
        "w",
        encoding="utf8",
    )
    index = 0
    report_tx = ""
    report_rx = ""
    cq_zone = ""
    itu_zone = ""
    number_tx = ""
    number_rx = ""
    comment = ""
    while index < len(log):
        if profile_type == "3":
            report_tx = f"Report: {log[index].report_tx}"
            report_rx = ""
        else:
            report_tx = f"Report TX: {log[index].report_tx}"
            report_rx = f"\nReport RX: {log[index].report_rx}"
        if len(log[index].cq_zone) == 0:
            cq_zone = ""
        else:
            cq_zone = f"CQ-zone: {log[index].cq_zone}, "
        if len(log[index].itu_zone) == 0:
            itu_zone = ""
        else:
            itu_zone = f"ITU-zone: {log[index].itu_zone}\n"
        if log[index].prog_number_tx == "":
            number_tx = ""
        else:
            number_tx = f"Progressive number TX: {log[index].prog_number_tx}\n"
        if log[index].prog_number_rx == "":
            number_rx = ""
        else:
            number_rx = f"Progressive number RX: {log[index].prog_number_rx}\n"
        if log[index].comment == "":
            comment = ""
        else:
            comment = f"Comment: {log[index].comment}\n"
        file.write(
            f"Callsign: {log[index].callsign}\n{report_tx}{report_rx}\nName: {log[index].name}\nQTH: {log[index].qth}\n{cq_zone}{itu_zone}Date: {log[index].date}\nBand / Frequency: {log[index].band}\nMode: {log[index].mode}\n{number_tx}{number_rx}{comment}\n"
        )
        file.flush()
        index += 1
    file.close()
    print(f"{index} records have beeen saved")


def export_all(log, profile_type):
    if not os.path.isdir(f"profiles/{profilename}/export"):
        os.mkdir(f"profiles/{profilename}/export")
    file = open(
        f"profiles/{profilename}/export/{profilename}.txt", "w", encoding="utf8"
    )
    counter = 0
    report_tx = ""
    report_rx = ""
    cq_zone = ""
    itu_zone = ""
    number_tx = ""
    number_rx = ""
    comment = ""
    for column in csv.DictReader(log, dialect="excel"):
        if profile_type == "3":
            report_tx = f'Report: {column["Report TX"]}'
            report_rx = ""
            column["Progressive number TX"] = ""
            column["Progressive number RX"] = ""
        else:
            report_tx = f'Report TX: {column["Report TX"]}'
            report_rx = f'\nReport RX: {column["Report RX"]}'
        if len(column["CQ-zone"]) == 0:
            cq_zone = ""
        else:
            cq_zone = f'CQ-zone: {column["CQ-zone"]}, '
        if len(column["ITU-zone"]) == 0:
            itu_zone = ""
        else:
            itu_zone = f'ITU-zone: {column["ITU-zone"]}\n'
        if column["Progressive number TX"] == "":
            number_tx = ""
        else:
            number_tx = f'Progressive number TX: {column["Progressive number TX"]}\n'
        if column["Progressive number RX"] == "":
            number_rx = ""
        else:
            number_rx = f'Progressive number RX: {column["Progressive number RX"]}\n'
        if column["Comments"] == "":
            comment = ""
        else:
            comment = f'Comment: {column["Comments"]}\n'
        file.write(
            f'Callsign: {column["Callsign"]}\n{report_tx}{report_rx}\nName: {column["Name"]}\nQTH: {column["QTH"]}\n{cq_zone}{itu_zone}Date: {column["Date"]}\nBand / Frequency: {column["Band / Frequency"]}\nMode: {column["Mode"]}\n{number_tx}{number_rx}{comment}\n'
        )
        file.flush()
        counter += 1
    file.close()
    print(f"{counter} records have beeen saved")


def select_band(band):
    selection = ""
    if len(band) > 0 and len(band) <= 3:
        selection = f"{band} m."
    else:
        selection = band
    if band != "" and not band.isdigit():
        selection = f"{band} band"
    return selection


def select_mode(mode):
    modulation = ""
    mode_list = {"1": "USB", "2": "LSB", "3": "CW", "4": "AM", "5": "FM", "6": "DIGI"}
    if mode_list.get(mode):
        modulation = mode_list[mode]
    else:
        modulation = mode
    return modulation


if not os.path.isdir("profiles"):
    os.mkdir("profiles")

welcome = "Welcome to Ham-Star Log!"
print(welcome.center(len(welcome) + 53, "*") + "\n")

while True:
    profilename = input("Enter profile name: ")[:20].lower()
    if os.path.isdir(f"profiles/{profilename}"):
        break
    else:
        create_profile = input(
            f'Can\'t find "{profilename}". Would you like to create a new profile? (<Y> - yes, <N> -no): '
        )[:1].lower()
    if create_profile == "y":
        new_profile(profilename)
        break

log_file = f"profiles/{profilename}/{profilename}.csv"
config = open(f"profiles/{profilename}/{profilename}.ini", "r", encoding="UTF8")
params = read_config(config, profilename)
config.close()
print(
    f'\tHello {params["name"]}.\nType "help" or "commands" to display commands list.\n'
)
time_begin = datetime.now()
if params["profiletype"] == "2":
    prefix_list = open("divs.csv", "r", newline="")
else:
    prefix_list = open("prefix_list.csv", "r", newline="")
contacts_counter = 0
number_tx = 1
set_band = ""
set_mode = ""
set_prog_numbers = "OFF"
command = ""
contacts_list = []
commands_list = (
    "BAND",
    "CLEAR",
    "CONTACTS",
    "COMMANDS",
    "COUNTER",
    "EXPORT",
    "HELP",
    "INFO",
    "MODE",
    "NUMBERS",
    "QSO",
    "SKIP",
    "STOP",
    "TIME",
)
contact_search = Logreader(prefix_list, params["profiletype"])

while True:
    log = open(log_file, "r", newline="", encoding="utf8")
    command = input("Enter command: ").upper()[:20].split()
    if len(command) == 1:
        command.append("")
    if command[0] == commands_list[0]:
        if command[1] == "":
            print('Parameter "band" or "frequency" is missing.\n')
            set_band = ""
        else:
            set_band = select_band(command[1])
            print(f"Band set to {set_band}\n")

    elif command[0] == commands_list[1]:
        os.system("clear")
        os.system("cls")

    elif command[0] == commands_list[2]:
        if command[1] == "ALL":
            contact_search.search(log)
            print(
                f"Log has {contact_search.all_contacts_counter} records, {contact_search.callsigns} callsigns and {contact_search.countries} countries.\n"
            )
        elif command[1] == "LAST":
            print(f"{contacts_counter} contacts.\n")
        else:
            print('Required parameter "all" or "last".\n')

    elif command[0] == commands_list[3]:
        print(
            "\t"
            + ", ".join(commands_list[0:5])
            + "\n\t"
            + ", ".join(commands_list[5:10])
            + "\n\t"
            + ", ".join(commands_list[10:13])
            + ".\n"
        )

    elif command[0] == commands_list[4]:
        set_prog_numbers="ON"
        if not command[1].isdigit():
            command[1] = "0"
        number_tx = int(command[1])
        print(f"progressive numbers set from {number_tx}.\n")
        number_tx += 1

    elif command[0] == commands_list[5]:
        if command[1] == "ALL":
            export_all(log, params["profiletype"])
        elif command[1] == "LAST":
            export_last(contacts_list, params["profiletype"])
        else:
            print('Required parameter "all" or "last".\n')

    elif command[0] == commands_list[6]:
        help(commands_list)

    elif command[0] == commands_list[7]:
        if command[1] == "":
            print('Parameter "callsign" is missing.\n')
        else:
            contact_search.search(log, command[1])
            print(contact_search.info)

    elif command[0] == commands_list[8]:
        if command[1] == "":
            print('Parameter "mode" is missing.\n')
        else:
            set_mode = select_mode(command[1])
            print(f"Mode set to {set_mode}.\n")

    elif command[0] == commands_list[9]:
        if set_prog_numbers == "OFF":
            set_prog_numbers = "ON"
            print(f"Progressive numbers {set_prog_numbers}.\n")
        elif set_prog_numbers == "ON":
            set_prog_numbers = "OFF"
            print(f"Progressive numbers {set_prog_numbers}.\n")

    elif command[0] == commands_list[10]:
        for _ in range(1):
            date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            if command[1] == "":
                callsign = input("*Callsign: ")[:20].upper()
            else:
                callsign = command[1]
            if (
                callsign == commands_list[11]
                or callsign == commands_list[12]
                or len(callsign) < 3
            ):
                callsign == ""
                break
            contact_search.country(callsign)
            contact_search.search(log, callsign)
            print(contact_search.last_contact)
            report_tx = input("Report TX: ")[:7].upper()
            if report_tx == commands_list[11] or report_tx == commands_list[12]:
                report_tx = ""
                break
            if set_prog_numbers == "ON" and params["profiletype"] != "3":
                print(f"Progressive number TX: ({str(number_tx).zfill(3)}")
            if params["profiletype"] == "1" or params["profiletype"] == "2":
                report_rx = input("Report RX: ")[:7].upper()
            else:
                report_rx = ""
            if report_rx == commands_list[11] or report_rx == commands_list[12]:
                report_rx = ""
                break
            if set_prog_numbers == "ON" and params["profiletype"] != "3":
                prog_number_rx = input("Progressive number RX: ")[:9].upper()
                prog_number_rx = prog_number_rx.zfill(3)
            else:
                prog_number_rx = ""
            if prog_number_rx == "000":
                prog_number_rx = ""
            if (
                prog_number_rx == commands_list[11]
                or prog_number_rx == commands_list[12]
            ):
                prog_number_rx = ""
                break
            if contact_search.name == "UNKNOWN" or contact_search.name == "":
                name = input("Name: ")[:20].title()
            else:
                name = contact_search.name
            if name == "Skip" or name == "Stop":
                name = ""
                break
            if name == "":
                name = "UNKNOWN"
            if len(contact_search.qth) > 0 and "UNKNOWN" not in contact_search.qth:
                qth = contact_search.qth
            if "UNKNOWN" in contact_search.qth or contact_search.qth == "":
                qth = input(f"QTH: {contact_search.country(callsign)} ")[:20].title()
                if qth == "":
                    qth = "UNKNOWN"
                qth = f"{qth}, {contact_search.country(callsign)}"
            if "Skip" in qth:
                qth = ""
                break
            cq_zone = contact_search.cq_zone
            itu_zone = contact_search.itu_zone
            if len(set_band) > 0:
                band = set_band
            else:
                while True:
                    band = select_band(input("*Band / Frequency: ")[:20].upper())
                    if band == "":
                        print('The field "Band / Frequency" must be filled')
                    else:
                        break
            if commands_list[11] in band:
                band = ""
                break
            if len(set_mode) > 0:
                mode = set_mode
            else:
                while True:
                    mode = select_mode(input("*Mode: ")[:10].upper())
                    if mode == "":
                        print('The field "Mode" must be filled')
                    else:
                        break
            if mode == commands_list[11] or mode == commands_list[12]:
                mode = ""
                break
            comment = input("Comment: ")[:200]
            if len(comment) > 0:
                comment = f'"{comment}"'
            if comment == commands_list[11] or comment == commands_list[12]:
                comment = ""
                break
            if mode == "CW" and report_tx == "":
                report_tx = "599"
            elif mode == "AM" and report_tx == "" or mode == "FM" and report_tx == "":
                report_tx = "595"
            if mode == "CW" and report_rx == "":
                report_rx = "599"
            elif mode == "AM" and report_rx == "" or mode == "FM" and report_rx == "":
                report_rx = "595"
            if report_tx == "":
                report_tx = "59"
            if report_rx == "":
                report_rx = "59"
            if set_prog_numbers == "ON":
                prog_number_tx = str(number_tx).zfill(3)
            else:
                prog_number_tx = ""
            contact = New_contact(
                callsign,
                report_tx,
                report_rx,
                name,
                qth,
                cq_zone,
                itu_zone,
                date,
                band,
                mode,
                prog_number_tx,
                prog_number_rx,
                comment,
            )
            contacts_list.append(contact)
            if set_prog_numbers == "ON":
                number_tx += 1

            if params["profiletype"] == "1" or params["profiletype"] == "2":
                record = (
                    contacts_list[contacts_counter].callsign,
                    contacts_list[contacts_counter].report_tx,
                    contacts_list[contacts_counter].report_rx,
                    contacts_list[contacts_counter].name,
                    contacts_list[contacts_counter].qth,
                    contacts_list[contacts_counter].cq_zone,
                    contacts_list[contacts_counter].itu_zone,
                    contacts_list[contacts_counter].date,
                    contacts_list[contacts_counter].band,
                    contacts_list[contacts_counter].mode,
                    contacts_list[contacts_counter].prog_number_tx,
                    contacts_list[contacts_counter].prog_number_rx,
                    contacts_list[contacts_counter].comment,
                )
            elif params["profiletype"] == "3":
                record = (
                    contacts_list[contacts_counter].callsign,
                    contacts_list[contacts_counter].report_tx,
                    contacts_list[contacts_counter].name,
                    contacts_list[contacts_counter].qth,
                    contacts_list[contacts_counter].cq_zone,
                    contacts_list[contacts_counter].itu_zone,
                    contacts_list[contacts_counter].date,
                    contacts_list[contacts_counter].band,
                    contacts_list[contacts_counter].mode,
                    contacts_list[contacts_counter].comment,
                )
            if os.path.isfile(log_file):
                log = open(log_file, "a", newline="", encoding="utf8")
            logwriter = csv.writer(log, dialect="excel")
            logwriter.writerow(record)

            log.flush()
            contacts_counter += 1
            print("Success!\n")
            log.close()
    elif command[0] == commands_list[11] or command[0] == commands_list[12]:
        break
    elif command[0] == commands_list[13]:
        delta = f"{datetime.now()-time_begin}".split(".")
        print(
            f'{datetime.now(timezone.utc).strftime("%H:%M")} UTC. Duration of the current session: {delta[0]}.\n'
        )
    else:
        print("Incorrect command or parameter.\n")

prefix_list.close()
