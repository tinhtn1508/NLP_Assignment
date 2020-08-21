ruleTable = {
    "ROOT": { "den": "root", "di": "root", "xuat_phat": "root"},
    "xuat_phat": {"nao": "which-query", "tu": "from-to"},
    "tu": {"thanh_pho": "to_loc", "<VAR-LOC>": "<var>name"},
    "den": { "nao": "which-query", "thanh_pho": "to-loc", "luc": "arrive-time", "<VAR-LOC>": "<var>name"},
    "di": {"nao": "which-query", "den": "to-city", "tu": "from-to", "thoi_gian" : "time-query", "xe_bus": "lsubj"},
    "nao": { "xe_bus": "lsubj", "xe": "lsubj", "nhung": "plural"},
    "xe_bus": {"<VAR-BUS>": "<var>name"},
    "thanh_pho": { "<VAR-LOC>": "<var>name" },
    "luc": { "<VAR-TIM>": "<var>time-hour" },
}

queryTable = {"ATIME": ["B1 hue 22:00hr",
                        "B2 hue 22:30hr",
                        "B3 ho_chi_minh 05:00hr",
                        "B4 ho_chi_minh 5:30hr",
                        "B5 da_nang 13:30hr",
                        "B6 da_nang 9:30hr",
                        "B7 ho_chi_minh 20:30hr"],
              "DTIME": ["B1 ho_chi_minh 10:00hr",
                        "B2 ho_chi_minh 12:30hr",
                        "B3 da_nang 19:00hr",
                        "B4 da_nang 17:30hr",
                        "B5 hue 8:30hr",
                        "B6 hue 5:30hr",
                        "B7 hue 8:30hr"],
              "RUN-TIME": ["B1 ho_chi_minh hue 12:00hr",
                           "B2 ho_chi_minh hue 10:00hr",
                           "B3 da_nang ho_chi_minh 14:00hr",
                           "B4 ho_chi_minh da_nang 12:00hr",
                           "B5 da_nang hue 5:00hr",
                           "B6 da_nang hue 4:00hr",
                           "B7 ho_chi_minh hue 12:00hr"]
              }

class Database():
    def __init__(self):
            pass
    def getBusNameFromLocation(self, location: str):
        out = []
        for i, atimeData in enumerate(queryTable["ATIME"]):
            if location in atimeData:
                out.append(atimeData.split()[0])
        return out

    def getBusNameToLocation(self, location: str):
        out = []
        for i, atimeData in enumerate(queryTable["DTIME"]):
            if location in atimeData:
                out.append(atimeData.split()[0])
        return out

    def getBusNameFromToLocation(self, fromLoc: str, toLoc: str):
        out = []
        for i, atimeData in enumerate(queryTable["ATIME"]):
            if fromLoc in atimeData:
                if toLoc in queryTable["DTIME"][i]:
                    out.append(atimeData.split()[0])
        return out

    def getBusFromDtimeAndToLocation(self, dTime: str, toLoc: str):
        out = []
        for i, atimeData in enumerate(queryTable["DTIME"]):
            if dTime in atimeData and toLoc in atimeData:
                out.append(atimeData.split()[0])
        return out

    def getTimeFromBusFromToLocation(self, busName: str, fromLoc: str, toLoc: str):
        out = []
        for runTimeData in queryTable["RUN-TIME"]:
            if busName in runTimeData and fromLoc in runTimeData and toLoc in runTimeData:
                out.append(runTimeData.split()[3])
        return out

# print(getBusNameFromLocation("hue"))
# print(getBusNameToLocation("hue"))
# print(getBusNameFromToLocation("da_nang", "hue"))
# print(getBusFromDtimeAndToLocation("8:30hr", "hue"))
# print(getTimeFromBusFromToLocation("B3", "da_nang", "ho_chi_minh"))
