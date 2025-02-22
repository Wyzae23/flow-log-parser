import csv
import argparse

# protocol mapping from 
# https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
protocolMap = {
    "0": "hopopt",
    "1": "icmp",
    "2": "igmp",
    "3": "ggp",
    "4": "ip",
    "5": "st",
    "6": "tcp",
    "7": "cbt",
    "8": "egp",
    "9": "igp",
    "10": "bbn-rcc-mon",
    "11": "nvp-ii",
    "12": "pup",
    "13": "argus",
    "14": "emcon",
    "15": "xnet",
    "16": "chaos",
    "17": "udp",
    "18": "mux",
    "19": "dcn-meas"
}

# removes extension from filename
def removeExtension(filename):
    parts = filename.split(".")
    if len(parts) == 1:
        return filename
    return '.'.join(parts[:-1])

# generates lookup table from csv input
def loadLookupTable(filepath):
    lookup = {}
    with open(filepath, "r", newline="") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            key = (row[0], row[1])
            lookup[key] = row[2]
    return lookup

# process each row of the flow log
def processFlowLogs(filepath, lookup):
    tagCounts = {}
    keyCounts = {}
    totalInputs = 0

    with open(filepath, "r", newline="") as f:
        for line in f:
            fields = line.split()

            # if there isn't exactly 14 fields in the row, it's invalid
            if not fields or len(fields) != 14:
                continue
            dstPort = fields[6]
            protocol = None

            # check if the protocol is in our protocolMap
            # if protocol isn't in mapping, then we can skip this row
            # as it's invalid
            if fields[7] in protocolMap:
                protocol = protocolMap[fields[7]]

            # for valid rows, process them
            if dstPort and protocol:
                totalInputs += 1
                key = (dstPort, protocol)
                keyCounts[key] = keyCounts.get(key, 0) + 1
                if key in lookup:
                    tag = lookup[key]
                    tagCounts[tag] = tagCounts.get(tag, 0) + 1
                    
        # generate "Untagged" count for the tagCounts map
        totalTagged = sum(tagCounts.values())
        if totalInputs > 0:
            tagCounts["Untagged"] = totalInputs - totalTagged

        return tagCounts, keyCounts
    
# generate a CSV with `filename`, with headers as `header`, and with row `rows`
def writeCSV(filename, header, rows):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)


def main ():
    # set up parser/arguments
    parser = argparse.ArgumentParser(description="Parsing input log file and lookup table")
    parser.add_argument("input_file")
    parser.add_argument("lookup_table")
    args = parser.parse_args()

    # grab filepaths for input file and lookup table
    lookupTableFilepath = args.lookup_table
    inputFilepath = args.input_file

    lookup = loadLookupTable(lookupTableFilepath)

    tagCounts, keyCounts = processFlowLogs(inputFilepath, lookup)
    
    # generate rows for tag counts output file
    tagRows = []
    for tag in tagCounts:
        tagRows.append([tag, tagCounts[tag]])
    tagCountsFilename = f"tag_counts_for_{removeExtension(lookupTableFilepath)}_and_{removeExtension(inputFilepath)}.csv"
    writeCSV(tagCountsFilename, ["Tag", "Count"], tagRows)
    print(f"Generated output CSV for {tagCountsFilename}")

    # generate rows for port protocol combination counts output file
    portProtocolRows = []
    for (dstPort, protocol) in keyCounts:
        portProtocolRows.append([dstPort, protocol, keyCounts[(dstPort, protocol)]])
    portProtocolCountsFilename = f"port_protocol_counts_for_{removeExtension(lookupTableFilepath)}_and_{removeExtension(inputFilepath)}.csv"
    writeCSV(portProtocolCountsFilename, ["Port", "Protocol", "Count"], portProtocolRows)
    print(f"Generated output CSV for {portProtocolCountsFilename}")

if __name__ == "__main__":
    main()