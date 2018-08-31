import csv, datetime

# Computing for a specific interval of time so we can go back in time
end = datetime.datetime.today()
daysInPastToLook = 7
start = end - datetime.timedelta(days=daysInPastToLook)

candidates = [ c for c in csv.DictReader(open("candidates.csv")) ]

# Convert string dates to real dates
dateKeys = ["Application Date", "Last Activity", "Last Stage Change", "Offer Date", "Start Date", "Rejection Date", "Next Scheduled Interview", "Last Scheduled Interview"]

for candidate in candidates:
    for dateKey in dateKeys:
        s = candidate[dateKey]
        if s:
            candidate[dateKey] = datetime.datetime.strptime(s, "%m/%d/%Y")

# Canonicalize on "Face to Face"
for candidate in candidates:
    if "Face to Face" in candidate["Stage"]:
        candidate["Stage"] = "Face to Face"

def isInDateRange(date, start, end):
    return date and date > start and date <= end

stagesInOrder = ["Application Review", "Match Talk", "Black Belt", "Sell Call", "Face to Face", "Reference Check", "Hiring Board", "Offer"]
stagesToHighlight = stagesInOrder[-4:]  # F2F onward

# Counters
applications = 0
rejections = 0
offers = 0
candidatesFinished = 0
daysToFinish = 0
stageCounts = dict.fromkeys(stagesInOrder, 0)
highlights = {}

# Process each candidate and see if they fit certain categories
for candidate in candidates:
    # Skip Denys Kurylenko - candidate that is on this req but is actually for SF benefits
    if candidate["Candidate ID"] == "74972570":
        continue

    # Did they apply in the time range?
    if isInDateRange(candidate["Application Date"], start, end):
        applications += 1

    # Did we reject in the time range?
    if isInDateRange(candidate["Rejection Date"], start, end):
        rejections += 1
        if candidate["Application Date"]:
            candidatesFinished += 1
            daysToFinish += (candidate["Rejection Date"] - candidate["Application Date"]).days

    # New offers
    if isInDateRange(candidate["Offer Date"], start, end):
        offers += 1
        if candidate["Application Date"]:
            candidatesFinished += 1
            daysToFinish += (candidate["Offer Date"] - candidate["Application Date"]).days

    # Count toward stages if active
    if candidate["Status"] == "Active":
        stageCounts[candidate["Stage"]] += 1

    # Highlight certain candidates in interesting stages
    if candidate["Status"] == "Active" and candidate["Stage"] in stagesToHighlight:
        if candidate["Stage"] not in highlights:
            highlights[candidate["Stage"]] = []
        highlights[candidate["Stage"]].append(candidate)

#################################
# Print to file
#################################
f = open("out.csv", "w")

# Stage counts
f.write("STAGE COUNTS\n")
for stage in stagesInOrder:
    f.write("%s,%i\n" % (stage, stageCounts[stage]))
f.write("\n")

# General stats
f.write("STATS (past 7d)\n")
f.write("New applications,%i\n" % (applications))
f.write("Rejections,%i\n" % (rejections))
f.write("Offers,%i\n" % (offers))
f.write("Avg. days in process,%f\n" % (float(daysToFinish) / candidatesFinished))
f.write("\n")

# Highlights
def printHighlightedCandidate(candidate, f):
    if candidate["Title"] and candidate["Company"]:
        f.write("  %s %s - %s @ %s\n" % (candidate["First Name"], candidate["Last Name"], candidate["Title"], candidate["Company"]))
    else:
        f.write("  %s %s\n" % (candidate["First Name"], candidate["Last Name"]))

f.write("HIGHLIGHTS\n")
for stage in stagesToHighlight:
    if stage in highlights:
        f.write("%s\n" % (stage))
        for candidate in highlights[stage]:
            printHighlightedCandidate(candidate, f)
f.write("\n")

f.close()
