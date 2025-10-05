from datetime import datetime, timezone
import csv
import os
import shutil
import re


class New_contact:
    def __init__(
        self,
        callsign,
        report_tx,
        report_rx,
        name,
        qth,
        gridsquare,
        cq_zone,
        itu_zone,
        date,
        band,
        frequency,
        mode,
        prog_number_tx,
        prog_number_rx,
        qsl_sent,
        qsl_rcvd,
        comment,
    ):
        self.callsign = callsign
        self.report_tx = report_tx
        self.report_rx = report_rx
        self.name = name
        self.qth = qth
        self.gridsquare = gridsquare
        self.cq_zone = cq_zone
        self.itu_zone = itu_zone
        self.date = date
        self.band = band
        self.frequency = frequency
        self.mode = mode
        self.prog_number_tx = prog_number_tx
        self.prog_number_rx = prog_number_rx
        self.qsl_sent = qsl_sent
        self.qsl_rcvd = qsl_rcvd
        self.comment = comment


class Logreader:
    def __init__(self, params, prefix_list):
        self.headers = headers
        self.params = params
        self.prefix_list = prefix_list

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

    def repr_date(date):
        if len(date) == 0:
            return
        date = date.split()
        months = (
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
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
        self.country(callsign)
        qso_counter = 0
        all_contacts_counter = 0
        tx = ""
        rx = ""
        name = ""
        qth = ""
        gridsquare = ""
        cq_zone = ""
        itu_zone = ""
        date = ""
        last_date = ""
        band = ""
        frequency = ""
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
        self.gridsquare = ""
        self.qsl_sent = ""
        self.qsl_rcvd = ""
        if len(self.cq_zone) > 0:
            cq_zone = f"\n\tCQ-zone: {self.cq_zone}, "
        if len(self.itu_zone) > 0:
            itu_zone = f"ITU-zone: {self.itu_zone}."
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
                tx = column["Report sent"]
                if self.params["profiletype"] == "3":
                    rx = ""
                else:
                    rx = column["Report RCVD"]
                self.name = column["Name"]
                if column["Name"] == "UNKNOWN":
                    name = ""
                else:
                    name = f'{column["Name"]}.'
                self.qth = column["QTH"]
                qth = f"{column['QTH']}"
                self.gridsquare = column["Gridsquare"]
                if len(column["Gridsquare"]) != 0:
                    gridsquare = f" ({column['Gridsquare']})."
                else:
                    gridsquare = ""
                date = column["Date"]
                band = column["Band"]
                if len(column["FREQ"]) != 0:
                    frequency = f" ({column['FREQ']})"
                else:
                    frequency = ""
                mode = column["Mode"]
                qsl_sent = column["QSL_SENT"]
                qsl_rcvd = column["QSL_RCVD"]
                comment = column["Comments"]
                if len(comment) != 0:
                    last_comment = f"\n\tLast comment: {comment}"
                    comment = f"\tComment: {comment}\n"
                if self.params["profiletype"] == "3":
                    info += f"{qso_counter}- {Logreader.repr_date(date)}. Report: {tx}. Band: {band}{frequency},{mode}.\n{comment}"
                else:
                    info += f"{qso_counter}- {Logreader.repr_date(date)}. TX: {tx}, RX: {rx}. Band: {band}{frequency},{mode}.\n{comment}"
        last_date = Logreader.repr_date(date)
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
        self.info = (
            f"\t{qso_counter} QSO. {name} {qth}{gridsquare}{cq_zone}{itu_zone}\n{info}"
        )
        if qso_counter == 0:
            if len(self.country(callsign)) > 0:
                cq_zone = f"CQ-zone: {self.cq_zone}, "
                itu_zone = f"ITU-zone: {self.itu_zone}."
            self.last_contact = f"\t{qso_counter} QSO. {qth} {cq_zone}{itu_zone}\n"
            self.info = f"\t{qso_counter} QSO. {qth}{gridsquare} {cq_zone}{itu_zone}\n"
        else:
            self.last_contact = f"\t{qso_counter} QSO. {name} {qth}{gridsquare}{cq_zone}{itu_zone}\nLast QSO: {last_date}. Band: {band}{frequency},{mode}.{last_comment}"


class Converters(Logreader):
    def __init__(self, headers):
        super().__init__(params, prefix_list)

    def old_log(self):
        new_log = []
        row = []
        blank = ""
        new_config = ["softwareversion=2.0\n"]
        log = open(
            f"profiles/{self.params['profilename']}/{self.params['profilename']}.csv",
            "r",
            newline="",
            encoding="utf8",
        )
        for column in csv.DictReader(log, dialect="excel"):
            if self.params["profiletype"] == "3":
                row = [
                    column["Callsign"],
                    column["Report TX"],
                    column["Name"],
                    column["QTH"],
                    blank,
                    column["CQ-zone"],
                    column["ITU-zone"],
                    column["Date"],
                    column["Band / Frequency"],
                    blank,
                    column["Mode"],
                    blank,
                    blank,
                    column["Comments"],
                ]
            else:
                row = [
                    column["Callsign"],
                    column["Report TX"],
                    column["Report RX"],
                    column["Name"],
                    column["QTH"],
                    blank,
                    column["CQ-zone"],
                    column["ITU-zone"],
                    column["Date"],
                    column["Band / Frequency"],
                    blank,
                    column["Mode"],
                    column["Progressive number TX"],
                    column["Progressive number RX"],
                    blank,
                    blank,
                    column["Comments"],
                ]
            new_log.append(row)
        log.close()
        log = open(
            f"profiles/{self.params['profilename']}/{self.params['profilename']}.csv",
            "w",
            newline="",
            encoding="utf8",
        )
        logwriter = csv.writer(log, dialect="excel")
        logwriter.writerow(headers)
        logwriter.writerows(new_log)
        log.close()
        config = open(
            f"profiles/{self.params['profilename']}/{self.params['profilename']}.ini",
            "r",
            encoding="UTF8",
        )
        for param in config:
            new_config.append(param)
        config.close()
        config = open(
            f"profiles/{self.params['profilename']}/{self.params['profilename']}.ini",
            "w",
            encoding="UTF8",
        )
        config.writelines(new_config)
        config.close()

    def export_last(self, log):
        if params["profiletype"] != "3":
            operator_adi = (
                f"<OPERATOR:{len(self.params['callsign'])}>{self.params['callsign']} "
            )
            operator_txt = self.params["callsign"]
        else:
            operator_adi = "<OPERATOR:3>SWL "
            operator_txt = "SWL"
        index = 0
        string_txt = ""
        string_adi = ""
        lines_txt = [
            f"\t\t\t\t* Generated by Ham-starLog version 2.0.\n\t\t\t\t* Creation date: {Logreader.repr_date(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))} UTC.\n\t\t\t\t* {operator_txt} log.\n\n",
        ]
        lines_adi = [
            "Generated by Ham-starLog V2.0\n<ADIF_VER:5>3.1.0\n<PROGRAMID:11>Ham-starLog\n<PROGRAMVERSION:3>2.0\n<EOH>\n\n",
        ]
        while index < len(log):
            date_adi = ""
            report_tx_txt = ""
            rst_sent_adi = ""
            report_rx_txt = ""
            rst_rcvd_adi = ""
            name_txt = ""
            name_adi = ""
            qth_txt = ""
            qth_adi = ""
            cq_zone_txt = ""
            itu_zone_txt = ""
            gridsquare_txt = ""
            gridsquare_adi = ""
            number_tx_txt = ""
            number_sent_adi = ""
            number_rx_txt = ""
            number_rcvd_adi = ""
            freq_txt = ""
            frequency_adi = ""
            comment_txt = ""
            comment_adi = ""
            date_adi = log[index].date.split(" ")
            new_date_adi = date_adi[0].replace("-", "")
            time_adi = date_adi[1].replace(":", "")
            qso_date_adi = f"<QSO_DATE:{len(new_date_adi)}>{new_date_adi} "
            time_on_adi = f"<TIME_ON:{len(time_adi)}>{time_adi} "
            call_adi = f"<CALL:{len(log[index].callsign)}>{log[index].callsign} "
            band_adi = f"<BAND:{len(log[index].band.replace(' ',''))}>{log[index].band.replace(' ','')} "
            mode_adi = f"<MODE:{len(log[index].mode)}>{log[index].mode} "
            qsl_sent_adi = (
                f"<QSL_SENT:{len(log[index].qsl_sent)}>{log[index].qsl_sent} "
            )
            qsl_rcvd_adi = (
                f"<QSL_RCVD:{len(log[index].qsl_rcvd)}>{log[index].qsl_rcvd} "
            )
            if self.params["profiletype"] == "3":
                report_tx_txt = f"Report: {log[index].report_tx}"
                report_rx_txt = ""
                rst_sent_adi = (
                    f"<RST_SENT:{len(log[index].report_tx)}>{log[index].report_tx} "
                )
                rst_rcvd_adi = ""
            else:
                report_tx_txt = f"Report sent: {log[index].report_tx}"
                report_rx_txt = f"\nReport RCVD: {log[index].report_rx}"
                rst_sent_adi = (
                    f"<RST_SENT:{len(log[index].report_tx)}>{log[index].report_tx} "
                )
                rst_rcvd_adi = (
                    f"<RST_RCVD:{len(log[index].report_rx)}>{log[index].report_rx} "
                )
            if len(log[index].cq_zone) != 0:
                cq_zone_txt = f"CQ-zone: {log[index].cq_zone}, "
            if len(log[index].itu_zone) != 0:
                itu_zone_txt = f"ITU-zone: {log[index].itu_zone}\n"
            if len(log[index].prog_number_tx) != 0:
                number_tx_txt = f"Progressive number TX: {log[index].prog_number_tx}\n"
                number_sent_adi = f"<NUMBER_SENT:{len(log[index].prog_number_tx)}>{log[index].prog_number_tx} "
            if len(log[index].prog_number_rx) != 0:
                number_rx_txt = f"Progressive number RX: {log[index].prog_number_rx}\n"
                number_rcvd_adi = f"<NUMBER_RCVD:{len(log[index].prog_number_rx)}>{log[index].prog_number_rx} "
            if len(log[index].comment) != 0:
                comment_txt = f"Comment: {log[index].comment}\n"
                comment_adi = (
                    f"<COMMENT:{len(log[index].comment)}>{log[index].comment} "
                )
            if log[index].name != "UNKNOWN":
                name_adi = f"<NAME:{len(log[index].name)}>{log[index].name} "
                name_txt = f"Name: {log[index].name}\n"
            qth_adi = log[index].qth.split(",")
            if qth_adi[0] == "UNKNOWN":
                qth_new_adi = ""
            else:
                qth_new_adi = f"<QTH:{len(qth_adi[0])}>{qth_adi[0]} "
            if len(log[index].gridsquare) != 0:
                gridsquare_txt = f"QTH locator: {log[index].gridsquare}\n"
                gridsquare_adi = (
                    f"<GRIDSQUARE:{len(log[index].gridsquare)}>{log[index].gridsquare} "
                )
            if len(log[index].frequency) != "":
                freq_txt = f"Frequency: {log[index].frequency}\n"
                frequency_adi = (
                    f"<FREQ:{len(log[index].frequency)}>{log[index].frequency} "
                )
            string_txt = f"\tCallsign: {log[index].callsign}\n{report_tx_txt}{report_rx_txt}\n{name_txt}QTH: {log[index].qth}\n{gridsquare_txt}{cq_zone_txt}{itu_zone_txt}Date: {log[index].date}\nBand: {log[index].band}\n{freq_txt}Mode: {log[index].mode}\n{number_tx_txt}{number_rx_txt}{comment_txt}\n"
            string_adi = f"{qso_date_adi}{time_on_adi}{call_adi}{band_adi}{frequency_adi}{mode_adi}{rst_sent_adi}{rst_rcvd_adi}{name_adi}{qth_new_adi}{gridsquare_adi}{operator_adi}{qsl_sent_adi}{qsl_rcvd_adi}{number_sent_adi}{number_rcvd_adi}{comment_adi}<EOR>\n"
            lines_txt.append(string_txt)
            lines_adi.append(string_adi)
            index += 1
        lines_txt.append("\t\t\t\t* END OF LOG *")
        file_txt = open(
            f'profiles/{self.params["profilename"]}/export/{datetime.now(timezone.utc).strftime("%Y-%m-%d")}_{operator_txt.lower()}(log).txt',
            "w",
            encoding="utf8",
        )
        file_txt.writelines(lines_txt)
        file_txt.close()
        file_adi = open(
            f'profiles/{self.params["profilename"]}/export/{datetime.now(timezone.utc).strftime("%Y-%m-%d")}_{operator_txt.lower()}(log).adi',
            "w",
            encoding="utf8",
        )
        file_adi.writelines(lines_adi)
        file_adi.close()
        print(f"{index} records have beeen saved")

    def export_all(self, log):
        if params["profiletype"] != "3":
            operator_adi = (
                f"<OPERATOR:{len(self.params['callsign'])}>{self.params['callsign']} "
            )
            operator_txt = self.params["callsign"]
        else:
            operator_adi = "<OPERATOR:3>SWL "
            operator_txt = "SWL"
        counter = 0
        lines_txt = [
            f"\t\t\t\t* Generated by Ham-starLog version 2.0.\n\t\t\t\t* Creation date: {Logreader.repr_date(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))} UTC.\n\t\t\t\t* {operator_txt} log.\n\n",
        ]
        lines_adi = [
            "Generated by Ham-starLog V2.0\n<ADIF_VER:5>3.1.0\n<PROGRAMID:11>Ham-starLog\n<PROGRAMVERSION:3>2.0\n<EOH>\n\n",
        ]
        string_txt = ""
        string_adi = ""
        for column in csv.DictReader(log, dialect="excel"):
            date_adi = ""
            report_tx_txt = ""
            rst_sent_adi = ""
            report_rx_txt = ""
            rst_rcvd_adi = ""
            name_txt = ""
            name_adi = ""
            qth_txt = ""
            qth_adi = ""
            cq_zone_txt = ""
            itu_zone_txt = ""
            gridsquare_txt = ""
            gridsquare_adi = ""
            number_tx_txt = ""
            number_sent_adi = ""
            number_rx_txt = ""
            number_rcvd_adi = ""
            freq_txt = ""
            frequency_adi = ""
            comment_txt = ""
            comment_adi = ""
            date_adi = column["Date"].split(" ")
            new_date_adi = date_adi[0].replace("-", "")
            time_adi = date_adi[1].replace(":", "")
            qso_date_adi = f"<QSO_DATE:{len(new_date_adi)}>{new_date_adi} "
            time_on_adi = f"<TIME_ON:{len(time_adi)}>{time_adi} "
            call_adi = f"<CALL:{len(column['Callsign'])}>{column['Callsign']} "
            band_adi = f"<BAND:{len(column['Band'].replace(' ',''))}>{column['Band'].replace(' ','')} "
            mode_adi = f"<MODE:{len(column['Mode'])}>{column['Mode']} "
            qsl_sent_adi = f"<QSL_SENT:{len(column['QSL_SENT'])}>{column['QSL_SENT']} "
            qsl_rcvd_adi = f"<QSL_RCVD:{len(column['QSL_RCVD'])}>{column['QSL_RCVD']} "
            if self.params["profiletype"] == "3":
                report_tx_txt = f'Report: {column["Report sent"]}'
                report_rx_txt = ""
                rst_sent_adi = (
                    f"<RST_SENT:{len(column['Report sent'])}>{column['Report sent']} "
                )
                rst_rcvd_adi = ""
                column["Progressive number TX"] = ""
                column["Progressive number RX"] = ""
            else:
                report_tx_txt = f'Report sent: {column["Report sent"]}'
                report_rx_txt = f'\nReport RCVD: {column["Report RCVD"]}'
                rst_sent_adi = (
                    f"<RST_SENT:{len(column['Report sent'])}>{column['Report sent']} "
                )
                rst_rcvd_adi = (
                    f"<RST_RCVD:{len(column['Report RCVD'])}>{column['Report RCVD']} "
                )
            if len(column["CQ-zone"]) != 0:
                cq_zone_txt = f'CQ-zone: {column["CQ-zone"]}, '
            if len(column["ITU-zone"]) != 0:
                itu_zone_txt = f'ITU-zone: {column["ITU-zone"]}\n'
            if len(column["Progressive number TX"]) != 0:
                number_tx_txt = (
                    f'Progressive number TX: {column["Progressive number TX"]}\n'
                )
                number_sent_adi = f"<NUMBER_SENT:{len(column['Progressive number TX'])}>{column['Progressive number TX']} "
            if len(column["Progressive number RX"]) != 0:
                number_rx_txt = (
                    f'Progressive number RX: {column["Progressive number RX"]}\n'
                )
                number_rcvd_adi = f"<NUMBER_RCVD:{len(column['Progressive number RX'])}>{column['Progressive number RX']} "
            if len(column["Comments"]) != 0:
                comment_txt = f'Comment: {column["Comments"]}\n'
                comment_adi = (
                    f"<COMMENT:{len(column['Comments'])}>{column['Comments']} "
                )
            if column["Name"] != "UNKNOWN":
                name_adi = f"<NAME:{len(column['Name'])}>{column['Name']} "
                name_txt = f"Name: {column['Name']}\n"
            qth_adi = column["QTH"].split(",")
            if qth_adi[0] == "UNKNOWN":
                qth_new_adi = ""
            else:
                qth_new_adi = f"<QTH:{len(qth_adi[0])}>{qth_adi[0]} "
            if len(column["Gridsquare"]) != 0:
                gridsquare_txt = f"QTH locator: {column['Gridsquare']}\n"
                gridsquare_adi = (
                    f"<GRIDSQUARE:{len(column['Gridsquare'])}>{column['Gridsquare']} "
                )
            if len(column["FREQ"]) != 0:
                freq_txt = f"Frequency: {column['FREQ']}\n"
                frequency_adi = f"<FREQ:{len(column['FREQ'])}>{column['FREQ']} "
            string_txt = f'\tCallsign: {column["Callsign"]}\n{report_tx_txt}{report_rx_txt}\n{name_txt}QTH: {column["QTH"]}\n{gridsquare_txt}{cq_zone_txt}{itu_zone_txt}Date: {column["Date"]}\nBand: {column["Band"]}\n{freq_txt}Mode: {column["Mode"]}\n{number_tx_txt}{number_rx_txt}{comment_txt}\n'
            string_adi = f"{qso_date_adi}{time_on_adi}{call_adi}{band_adi}{frequency_adi}{mode_adi}{rst_sent_adi}{rst_rcvd_adi}{name_adi}{qth_new_adi}{gridsquare_adi}{operator_adi}{qsl_sent_adi}{qsl_rcvd_adi}{number_sent_adi}{number_rcvd_adi}{comment_adi}<EOR>\n"
            lines_txt.append(string_txt)
            lines_adi.append(string_adi)
            counter += 1
        lines_txt.append("\t\t\t\t* END OF LOG *")
        file_txt = open(
            f"profiles/{self.params['profilename']}/export/{operator_txt.lower()}(log).txt",
            "w",
            encoding="utf8",
        )
        file_txt.writelines(lines_txt)
        file_txt.close()
        file_adi = open(
            f"profiles/{self.params['profilename']}/export/{operator_txt.lower()}(log).adi",
            "w",
            encoding="utf8",
        )
        file_adi.writelines(lines_adi)
        file_adi.close()
        print(f"{counter} records have beeen saved")

    def import_log(self):
        def parse_adi_record(record):
            fields = {}
            pattern = re.compile(r"<([^:>]+):(\d+)[^>]*>([^<]*)", re.IGNORECASE)
            for match in pattern.finditer(record):
                tag, length, value = match.groups()
                fields[tag.upper()] = value.strip()
            return fields

        if os.path.isfile(f"profiles/{self.params['profilename']}/import/log.adi"):
            file_adi = open(
                f"profiles/{self.params['profilename']}/import/log.adi",
                "r",
                encoding="utf8",
            )
        else:
            print(
                f'File "profiles/{self.params["profilename"]}/import/log.adi" is missing.\n'
            )
            return

        content = file_adi.read()
        row = ""
        rows = []

        if "<EOH>" in content:
            content = content.split("<EOH>")[1]

        records = content.split("<EOR>")
        qso_data = [parse_adi_record(record) for record in records if record.strip()]

        for qso in qso_data:
            callsign = ""
            report_sent = ""
            report_rcvd = ""
            name = ""
            qth = ""
            country = ""
            gridsquare = ""
            cq_zone = ""
            itu_zone = ""
            date = ""
            time = ""
            band = ""
            freq = ""
            mode = ""
            progressive_number_tx = ""
            progressive_number_rx = ""
            qsl_sent = ""
            qsl_rcvd = ""
            comments = ""
            country = self.country(qso["CALL"])
            if qso.get("TIME_ON") != None:
                time = (
                    qso["TIME_ON"][:2]
                    + ":"
                    + qso["TIME_ON"][2:4]
                    + ":"
                    + qso["TIME_ON"][4:]
                )
            if qso.get("QSO_DATE") != None:
                date = (
                    qso["QSO_DATE"][:4]
                    + "-"
                    + qso["QSO_DATE"][4:6]
                    + "-"
                    + qso["QSO_DATE"][6:]
                    + " "
                    + time
                )
            if qso.get("CALL") != None:
                callsign = qso["CALL"]
            if qso.get("BAND") != None:
                band = qso["BAND"]
            if qso.get("FREQ") != None:
                freq = qso["FREQ"].replace(".", "")
            if qso.get("MODE") != None:
                mode = qso["MODE"]
            if qso.get("RST") != None:
                report_sent = qso["RST"]
            if qso.get("RST_SENT") != None:
                report_sent = qso["RST_SENT"]
            if qso.get("RST_RCVD") != None:
                report_rcvd = qso["RST_RCVD"]
            if qso.get("NAME") == None:
                name = "UNKNOWN"
            else:
                name = qso["NAME"]
            if qso.get("QTH") == None:
                qth = f"UNKNOWN,{country}"
            else:
                qth = f"{qso['QTH']}, {country}"
            if qso.get("GRIDSQUARE") != None:
                gridsquare = qso["GRIDSQUARE"]
            cq_zone = self.cq_zone
            itu_zone = self.itu_zone
            if qso.get("QSL_SENT") != None:
                qsl_sent = qso["QSL_SENT"]
            if qso.get("QSL_RCVD") != None:
                qsl_rcvd = qso["QSL_RCVD"]
            if qso.get("NUMBER_SENT") != None:
                progressive_number_tx = qso["NUMBER_SENT"]
            if qso.get("NUMBER_RCVD") != None:
                progressive_number_rx = qso["NUMBER_RCVD"]
            if qso.get("COMMENT") != None:
                comments = qso["COMMENT"]
            if self.params["profiletype"] == "3":
                row = [
                    callsign,
                    report_sent,
                    name,
                    qth,
                    gridsquare,
                    cq_zone,
                    itu_zone,
                    date,
                    band,
                    freq,
                    mode,
                    qsl_sent,
                    qsl_rcvd,
                    comments,
                ]
            else:
                row = [
                    callsign,
                    report_sent,
                    report_rcvd,
                    name,
                    qth,
                    gridsquare,
                    cq_zone,
                    itu_zone,
                    date,
                    band,
                    freq,
                    mode,
                    progressive_number_tx,
                    progressive_number_rx,
                    qsl_sent,
                    qsl_rcvd,
                    comments,
                ]
            rows.append(row)
        file_adi.close()
        shutil.copy2(
            f"profiles/{self.params['profilename']}/{self.params['profilename']}.csv",
            f"profiles/{self.params['profilename']}/backup/{self.params['profilename']}.csv",
        )
        log = open(
            f"profiles/{self.params['profilename']}/{self.params['profilename']}.csv",
            "w",
            newline="",
            encoding="utf8",
        )
        logwriter = csv.writer(log, dialect="excel")
        logwriter.writerow(headers)
        logwriter.writerows(rows)
        log.close()
        print(f"{len(rows)} records has been imported.\n")


def validation(string):
    string = "".join(string)
    incorrect_characters = (
        "!",
        "~",
        "@",
        "#",
        "$",
        "%",
        "^",
        "&",
        "*",
        "(",
        ")",
        "_",
        "+",
        "=",
        "|",
        "\\",
        ".",
        "?",
        ">",
        "<",
        ",",
        '"',
        ";",
        ":",
    )
    for char in string:
        if char in incorrect_characters:
            print(f'Invalid character "{char}"!')
            return False
    return True


def help(commands_list):
    print(
        f"-{commands_list[0]} (band / frequency): set band or frequency;\n-{commands_list[1]}: clear display;\n-{commands_list[2]} (all, last): show log statistic;\n-{commands_list[3]}: display commands list;\n-{commands_list[4]} (number): set initial progressive number of the counter;\n-{commands_list[5]}: Exit programm;\n-{commands_list[6]} (all, last): export log to ADIF format;\n-{commands_list[7]}: (band / frequency): set band or frequency;\n-{commands_list[8]}: display this help;\n-{commands_list[9]}: Import log from ADIF format;\n-{commands_list[10]} (callsign, log): display all records with the operator, log statistic;\n-{commands_list[11]} (mode): set mode;\n-{commands_list[12]}: turn on / off progressive numbers;\n-{commands_list[13]} (callsign): create a new record;\n-{commands_list[14]}: skip contact;\n-{commands_list[15]}: exit programm;\n-{commands_list[16]}: display time UTC and duration the current session."
    )


def new_profile(profilename, log_columns, log_swl_columns):
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
    os.mkdir(f"profiles/{profilename}")
    os.mkdir(f"profiles/{profilename}/backup")
    os.mkdir(f"profiles/{profilename}/export")
    os.mkdir(f"profiles/{profilename}/import")
    config = open(f"profiles/{profilename}/{profilename}.ini", "w", encoding="UTF8")
    config.write(
        f"softwareversion=2.0\nprofilename={profilename}\nprofiletype={profile_type}\nname={username}\ncallsign={user_callsign}\nqth=\n"
    )
    config.close()
    log = open(
        f"profiles/{profilename}/{profilename}.csv", "w", encoding="UTF8", newline=""
    )
    logwriter = csv.writer(log, dialect="excel")
    if profile_type == "1" or profile_type == "2":
        logwriter.writerow(log_columns)
    elif profile_type == "3":
        logwriter.writerow(log_swl_columns)
        log.close()


def read_config(config, profilename):
    params = {}
    for parameter in config:
        params[parameter.split("=")[0]] = parameter.split("=")[1].strip("\n")
    return params


def select_band(band_freq):
    band = ""
    repr_band_freq = ""
    freq = ""
    freqs = ""
    bands_list = {
        "LW": "(100 - 520 kHz)",
        "MW": "(520 - 1602 kHz)",
        "160M": "(1810 - 2000 kHz)",
        "120M": "(2300 - 2495 kHz)",
        "90M": "(3200 - 3400 kHz)",
        "80M": "(3500 - 3900 kHz)",
        "75M": "(3900 - 4000 kHz)",
        "60M": "(4750 - 5450 kHz)",
        "49M": "(5900 - 6200 kHz)",
        "40M": "(7000 - 7200 kHz)",
        "41M": "(7100 - 7400 kHz)",
        "31M": "(9400 - 9900 kHz)",
        "30M": "(10100 - 10150 kHz)",
        "25M": "(11600 - 12100 kHz)",
        "22M": "(13570 - 13870 kHz)",
        "20M": "(14000 - 14350 kHz)",
        "19M": "(15100 - 15800 kHz)",
        "16M": "(17480 - 17900 kHz)",
        "17M": "(17900 - 18168 kHz)",
        "15M": "(21000 - 21450 kHz)",
        "13M": "(21450 - 21850 kHz)",
        "12M": "(24890 - 24990 kHz)",
        "11M": "(25600 - 28000 kHz)",
        "CB": "(26100 - 28000 kHz)",
        "10M": "(28000 - 30000 kHz)",
        "SW": "(1000 - 30000 kHz)",
        "LOWBAND": "(30000 - 50000 kHz)",
        "6M": "(50000 - 54000 kHz)",
        "4M": "(70000 - 70500 kHz)",
        "BROADCASTING": "(66000 - 74000 kHz)",
        "FM": "(87000 - 108000 kHz)",
        "AVIA": "108000 - 137000 kHz)",
        "2M": "144000 - 146000 kHz)",
        "VHF": "(30000 - 300000 kHz)",
        "70CM": "(430000 - 440000 kHz)",
        "PMR": "(446000 - 446100 kHz)",
        "UHF": "(300000 - 3000000 kHz)",
    }
    if band_freq != "" and not band_freq.isdigit():
        band = band_freq
    elif band_freq == "160":
        band = "160M"
    elif band_freq == "70":
        band = "70CM"
    elif len(band_freq) > 0 and len(band_freq) <= 2:
        band = f"{band_freq}M"
    else:
        freq = band_freq
    if len(freq) != 0:
        if int(freq) >= 100 and int(freq) < 520:
            band = "LW"
        elif int(freq) >= 520 and int(freq) <= 1602:
            band = "MW"
        elif int(freq) >= 1810 and int(freq) <= 2000:
            band = "160M"
        elif int(freq) >= 2300 and int(freq) <= 2495:
            band = "120M"
        elif int(freq) >= 3200 and int(freq) <= 3400:
            band = "90M"
        elif int(freq) >= 3500 and int(freq) < 3900:
            band = "80M"
        elif int(freq) >= 3900 and int(freq) <= 4000:
            band = "75M"
        elif int(freq) >= 4750 and int(freq) < 5000:
            band = "60M"
        elif int(freq) >= 5000 and int(freq) <= 5450:
            band = "60M"
        elif int(freq) >= 5900 and int(freq) <= 6200:
            band = "49M"
        elif int(freq) >= 7000 and int(freq) < 7200:
            band = "40M"
        elif int(freq) >= 7200 and int(freq) <= 7400:
            band = "41M"
        elif int(freq) >= 9400 and int(freq) <= 9900:
            band = "31M"
        elif int(freq) >= 10100 and int(freq) <= 10150:
            band = "30M"
        elif int(freq) >= 11600 and int(freq) <= 12100:
            band = "25M"
        elif int(freq) >= 13570 and int(freq) <= 13870:
            band = "22M"
        elif int(freq) >= 14000 and int(freq) <= 14350:
            band = "20M"
        elif int(freq) >= 15100 and int(freq) <= 15800:
            band = "19M"
        elif int(freq) >= 17480 and int(freq) < 17900:
            band = "16M"
        elif int(freq) >= 17900 and int(freq) <= 18168:
            band = "17M"
        elif int(freq) >= 18900 and int(freq) <= 19020:
            band = "15M"
        elif int(freq) >= 21000 and int(freq) < 21450:
            band = "15M"
        elif int(freq) >= 21450 and int(freq) <= 21850:
            band = "13M"
        elif int(freq) >= 24890 and int(freq) <= 24990:
            band = "12M"
        elif int(freq) >= 25600 and int(freq) < 26100:
            band = "11M"
        elif int(freq) >= 26100 and int(freq) <= 28000:
            band = "CB"
        elif int(freq) >= 28000 and int(freq) <= 30000:
            band = "10M"
        elif int(freq) >= 1000 and int(freq) <= 30000:
            band = "SW"
        elif int(freq) > 30000 and int(freq) < 50000:
            band = "LOWBAND"
        elif int(freq) >= 50000 and int(freq) <= 54000:
            band = "6M"
        elif int(freq) >= 70000 and int(freq) <= 70500:
            band = "4M"
        elif int(freq) >= 66000 and int(freq) <= 74000:
            band = "BROADCASTING"
        elif int(freq) >= 87000 and int(freq) <= 108000:
            band = "BROADCASTING(FM)"
        elif int(freq) > 108000 and int(freq) < 137000:
            band = "AVIA"
        elif int(freq) >= 144000 and int(freq) <= 146000:
            band = "2M"
        elif int(freq) > 54000 and int(freq) < 300000:
            band = "VHF"
        elif int(freq) >= 430000 and int(freq) <= 440000:
            band = "70CM"
        elif int(freq) >= 446000 and int(freq) <= 446100:
            band = "PMR"
        elif int(freq) >= 300000 and int(freq) <= 3000000:
            band = "UHF"
    if bands_list.get(band) != None:
        freqs = f" {bands_list[band]}"
    if len(band) > 0 and len(freq) > 0:
        repr_band_freq = f"{band} ({freq} kHz)."
    elif len(band) == 0 and len(freq) > 0:
        repr_band_freq = f"{freq} kHz."
    elif len(band) > 0 and len(freq) == 0:
        repr_band_freq = f"{band}{freqs}."
    else:
        repr_band_freq = ""
    return band, freq, repr_band_freq


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

log_columns = [
    "Callsign",
    "Report sent",
    "Report RCVD",
    "Name",
    "QTH",
    "Gridsquare",
    "CQ-zone",
    "ITU-zone",
    "Date",
    "Band",
    "FREQ",
    "Mode",
    "Progressive number TX",
    "Progressive number RX",
    "QSL_SENT",
    "QSL_RCVD",
    "Comments",
]
log_swl_columns = [
    "Callsign",
    "Report sent",
    "Name",
    "QTH",
    "Gridsquare",
    "CQ-zone",
    "ITU-zone",
    "Date",
    "Band",
    "FREQ",
    "Mode",
    "QSL_SENT",
    "QSL_RCVD",
    "Comments",
]
welcome = "Welcome to Ham-starLog!"
print(welcome.center(len(welcome) + 53, "*") + "\n")

while True:
    while True:
        profilename = input("Enter profile name: ")[:20].lower()
        if validation(profilename):
            break
    if os.path.isdir(f"profiles/{profilename}"):
        break
    else:
        create_profile = input(
            f'Profile "{profilename}" not found. Would you like to create a new profile? (<Y> - yes, <N> -no): '
        )[:1].lower()
    if create_profile == "y":
        new_profile(profilename, log_columns, log_swl_columns)
        break

if not os.path.isdir(f"profiles/{profilename}/backup"):
    os.mkdir(f"profiles/{profilename}/backup")
if not os.path.isdir(f"profiles/{profilename}/export"):
    os.mkdir(f"profiles/{profilename}/export")
if not os.path.isdir(f"profiles/{profilename}/import"):
    os.mkdir(f"profiles/{profilename}/import")
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
if params["profiletype"] == "3":
    headers = log_swl_columns
else:
    headers = log_columns
contacts_counter = 0
number_tx = 1
set_band = ""
set_frequency = ""
set_mode = ""
set_prog_numbers = "OFF"
gridsquare = ""
command = ""
qsl_sent = "Y"
qsl_rcvd = "N"
contacts_list = []
commands_list = (
    "BAND",
    "CLEAR",
    "CONTACTS",
    "COMMANDS",
    "COUNTER",
    "EXIT",
    "EXPORT",
    "FREQ",
    "HELP",
    "IMPORT",
    "INFO",
    "MODE",
    "NUMBERS",
    "QSO",
    "SKIP",
    "STOP",
    "TIME",
)
contact_search = Logreader(params, prefix_list)
converter = Converters(headers)
if params.get("softwareversion") == None:
    converter.old_log()

while True:
    log = open(log_file, "r", newline="", encoding="utf8")
    if params["profilename"] != profilename:
        input("\tInvalid config data!")
        break
    command = input("Enter command: ").upper()[:50].split()
    if len(command) == 1:
        command.append("")
    command[1] = " ".join(command[1:])
    if not validation(command):
        command = ["", ""]

    if command[0] == commands_list[0] or command[0] == commands_list[7]:
        if command[1] == "":
            print('Parameter "band" or "frequency" is missing.\n')
            set_band = ""
        else:
            set_band = select_band(command[1])[0]
            set_frequency = select_band(command[1])[1]
            print(f"Band set to {select_band(command[1])[2]}\n")

    elif command[0] == commands_list[1]:
        os.system("cls") if os.name == "nt" else os.system("clear")

    elif command[0] == commands_list[2]:
        if command[1] == "ALL":
            contact_search.search(log)
            print(
                f"Log contains {contact_search.all_contacts_counter} records, {contact_search.callsigns} callsigns and {contact_search.countries} countries.\n"
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
            + ", ".join(commands_list[10:15])
            + "\n\t"
            + ", ".join(commands_list[15:17])
            + ".\n"
        )

    elif command[0] == commands_list[4]:
        set_prog_numbers = "ON"
        if not command[1].isdigit():
            command[1] = "0"
        number_tx = int(command[1])
        print(f"progressive numbers set from {number_tx}.\n")
        number_tx += 1

    elif command[0] == commands_list[5]:
        print("\t Goodbye!")
        break

    elif command[0] == commands_list[6]:
        if command[1] == "ALL":
            converter.export_all(log)
        elif command[1] == "LAST":
            converter.export_last(contacts_list)
        else:
            print('Required parameter "all" or "last".\n')

    elif command[0] == commands_list[8]:
        help(commands_list)

    elif command[0] == commands_list[9]:
        while True:
            if (
                input(
                    'Would you like to import data from "log.adi"? ("Y" - yes, "N" - no):'
                ).upper()
                == "Y"
            ):
                converter.import_log()
                break
            else:
                print("Cancelled.\n")
                break

    elif command[0] == commands_list[10]:
        if command[1] == "":
            print('Parameter "callsign" or "log" is missing.\n')
        elif command[1] == "LOG":
            contact_search.search(log)
            print(
                f"Log contains {contact_search.all_contacts_counter} records, {contact_search.callsigns} callsigns and {contact_search.countries} countries.\n"
            )
        else:
            contact_search.search(log, command[1])
            print(contact_search.info)

    elif command[0] == commands_list[11]:
        if command[1] == "":
            print('Parameter "mode" is missing.\n')
        else:
            set_mode = select_mode(command[1])
            print(f"Mode set to {set_mode}.\n")

    elif command[0] == commands_list[12]:
        if set_prog_numbers == "OFF":
            set_prog_numbers = "ON"
            print(f"Progressive numbers {set_prog_numbers}.\n")
        elif set_prog_numbers == "ON":
            set_prog_numbers = "OFF"
            print(f"Progressive numbers {set_prog_numbers}.\n")

    elif command[0] == commands_list[13]:
        for _ in range(1):
            date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            if command[1] == "" and params["profiletype"] == "3":
                callsign = input("*Station name or callsign: ")[:30].strip().upper()
            elif command[1] == "":
                callsign = input("*Callsign: ")[:30].strip().upper()
            else:
                callsign = command[1]
            if (
                callsign == commands_list[14]
                or callsign == commands_list[15]
                or len(callsign) < 3
            ):
                callsign == ""
                break
            contact_search.country(callsign)
            contact_search.search(log, callsign)
            print(contact_search.last_contact)
            report_tx = input("Report Send: ")[:7].upper()
            if report_tx == commands_list[14] or report_tx == commands_list[15]:
                report_tx = ""
                break
            if set_prog_numbers == "ON" and params["profiletype"] != "3":
                print(f"Progressive number send: ({str(number_tx).zfill(3)}")
            if params["profiletype"] == "1" or params["profiletype"] == "2":
                report_rx = input("Report RCVD: ")[:7].upper()
            else:
                report_rx = ""
            if report_rx == commands_list[14] or report_rx == commands_list[15]:
                report_rx = ""
                break
            if set_prog_numbers == "ON" and params["profiletype"] != "3":
                prog_number_rx = input("Progressive number RCVD: ")[:9].upper()
                prog_number_rx = prog_number_rx.zfill(3)
            else:
                prog_number_rx = ""
            if prog_number_rx == "000":
                prog_number_rx = ""
            if (
                prog_number_rx == commands_list[14]
                or prog_number_rx == commands_list[15]
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
            if len(contact_search.gridsquare) > 0:
                gridsquare = contact_search.gridsquare
            else:
                gridsquare = input("Gridsquare (optional): ")[:8].upper()
            if gridsquare == commands_list[14] or gridsquare == commands_list[15]:
                gridsquare = ""
                break
            cq_zone = contact_search.cq_zone
            itu_zone = contact_search.itu_zone
            if len(set_band) > 0:
                band = set_band
                frequency = set_frequency
            else:
                while True:
                    while True:
                        band_tmp = input("*Band / Frequency (kHz): ")[:20].upper()
                        if validation(band_tmp):
                            band = select_band(band_tmp)[0]
                            frequency = select_band(band_tmp)[1]
                            break
                    if band_tmp == "":
                        print('The field "Band / Frequency" must be filled')
                    else:
                        break
            if band == commands_list[14] or band == commands_list[15]:
                band = ""
                frequency = ""
                break
            if len(set_mode) > 0:
                mode = set_mode
            else:
                while True:
                    while True:
                        mode = select_mode(input("*Mode: ")[:10].upper())
                        if validation(mode):
                            break
                    if mode == "":
                        print('The field "Mode" must be filled')
                    else:
                        break
            if mode == commands_list[14] or mode == commands_list[15]:
                mode = ""
                break
            comment = input("Comment: ")[:200]
            if len(comment) > 0:
                comment = f'"{comment}"'
            if comment == commands_list[14] or comment == commands_list[15]:
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
                gridsquare,
                cq_zone,
                itu_zone,
                date,
                band,
                frequency,
                mode,
                prog_number_tx,
                prog_number_rx,
                qsl_sent,
                qsl_rcvd,
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
                    contacts_list[contacts_counter].gridsquare,
                    contacts_list[contacts_counter].cq_zone,
                    contacts_list[contacts_counter].itu_zone,
                    contacts_list[contacts_counter].date,
                    contacts_list[contacts_counter].band,
                    contacts_list[contacts_counter].frequency,
                    contacts_list[contacts_counter].mode,
                    contacts_list[contacts_counter].prog_number_tx,
                    contacts_list[contacts_counter].prog_number_rx,
                    contacts_list[contacts_counter].qsl_sent,
                    contacts_list[contacts_counter].qsl_rcvd,
                    contacts_list[contacts_counter].comment,
                )
            elif params["profiletype"] == "3":
                record = (
                    contacts_list[contacts_counter].callsign,
                    contacts_list[contacts_counter].report_tx,
                    contacts_list[contacts_counter].name,
                    contacts_list[contacts_counter].qth,
                    contacts_list[contacts_counter].gridsquare,
                    contacts_list[contacts_counter].cq_zone,
                    contacts_list[contacts_counter].itu_zone,
                    contacts_list[contacts_counter].date,
                    contacts_list[contacts_counter].band,
                    contacts_list[contacts_counter].frequency,
                    contacts_list[contacts_counter].mode,
                    contacts_list[contacts_counter].qsl_sent,
                    contacts_list[contacts_counter].qsl_rcvd,
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
    elif command[0] == commands_list[14] or command[0] == commands_list[15]:
        print("\t Goodbye!")
        break
    elif command[0] == commands_list[16]:
        delta = f"{datetime.now()-time_begin}".split(".")
        print(
            f'{datetime.now(timezone.utc).strftime("%H:%M")} UTC. Duration of the current session: {delta[0]}.\n'
        )
    else:
        print("Incorrect command or parameter.\n")

prefix_list.close()
