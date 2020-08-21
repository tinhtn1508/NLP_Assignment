import re

ruleTable = {
    "ROOT": { "den": "root", "di": "root", "xuat_phat": "root"},
    "xuat_phat": {"nao": "which-query", "tu": "from-loc"},
    "tu": {"thanh_pho": "to_loc", "<VAR-LOC>": "<var>name"},
    "den": { "nao": "which-query", "thanh_pho": "to-loc", "luc": "arrive-time", "<VAR-LOC>": "<var>name"},
    "di": {"nao": "which-query", "den": "to-city", "tu": "from-loc", "thoi_gian" : "time-query", "xe_bus": "lsubj"},
    "nao": { "xe_bus": "lsubj", "xe": "lsubj", "nhung": "plural"},
    "xe_bus": {"<VAR-BUS>": "<var>name"},
    "thanh_pho": { "<VAR-LOC>": "<var>name" },
    "luc": { "<VAR-TIM>": "<var>time-hour" },
}

queryTable = {  "BUS": ["B1",
                        "B2",
                        "B3",
                        "B4"],
                "ATIME": [
                        "B1 HUE 22:00HR",
                        "B2 HUE 22:30HR",
                        "B3 HCMC 05:00HR",
                        "B4 HCMC 5:30HR",
                        "B5 DANANG 13:30HR",
                        "B6 DANANG 9:30HR",
                        "B7 HCMC 20:30HR"],
                "DTIME": [
                        "B1 HCMC 10:00HR",
                        "B2 HCMC 12:30HR",
                        "B3 DANANG 19:00HR",
                        "B4 DANANG 17:30HR",
                        "B5 HUE 8:30HR",
                        "B6 HUE 5:30HR",
                        "B7 HUE 8:30HR"],
                "RUN-TIME": [
                        "B1 HCMC HUE 12:00HR",
                        "B2 HCMC HUE 10:00HR",
                        "B3 DANANG HCMC 14:00HR",
                        "B4 HCMC DANANG 12:00HR",
                        "B5 DANANG HUE 5:00HR",
                        "B6 DANANG HUE 4:00HR",
                        "B7 HCMC HUE 12:00HR"]
                }
class Database():
    def __init__(self):
            self.bus = False
            self.aTime = None
            self.dTime = None
            self.runTime = None

    def getIndexVar(self, formatVar):
        for i, str in enumerate(formatVar):
            if "?" in str:
                return i

    def getTable(self, tableType):
        if tableType == "RUN-TIME":
            return self.runTime
        elif tableType == "DTIME":
            return self.dTime
        elif tableType == "ATIME":
            return self.aTime
        else:
            pass

    def getValueVar(self, tableType):
        index = self.getIndexVar(self.getTable(tableType))
        out = []
        for indexQuery, query in enumerate(queryTable[tableType]):
            isMatch = True
            for i, str in enumerate(self.getTable(tableType)):
                if "?" in str:
                    continue
                if str not in query:
                    isMatch = False
                    break
            if isMatch is True:
                out.append(query.split()[index])
        return out


    def process(self, queryStr: str):
        querySplit = queryStr.split()
        if len(querySplit) < 11:
            raise Exception("Invalid queryStr = {}".format(queryStr))

        for i in range(len(querySplit)):
            if querySplit[i] == "BUS":
                self.bus = True
            elif querySplit[i] == "RUN-TIME":
                self.runTime = querySplit[i+1:i+5]
            elif querySplit[i] == "ATIME":
                self.aTime = querySplit[i+1:i+4]
            elif querySplit[i] == "DTIME":
                self.dTime = querySplit[i+1:i+4]

        out = []
        if self.bus is True:
            out.append(queryTable["BUS"])
        if self.runTime is not None:
            out.append(self.getValueVar("RUN-TIME"))
        if self.aTime is not None:
            out.append(self.getValueVar("ATIME"))
        if self.dTime is not None:
            out.append(self.getValueVar("DTIME"))

        if len(out) == 0:
            return None
        elif len(out) == 1:
            return out[0]
        else:
            tmp = list(set.intersection(*[set(x) for x in out]))
            return None if len(tmp) == 0 else tmp
