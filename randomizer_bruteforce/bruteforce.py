"""
    This is very specialized, I cut a lot of code for other options/modes
    Future seed, when F3 star is fixed: 178957
"""
import sys
import multiprocessing
import signal

PROB_BOTH_HUBS = 25
ALL_MARKERS = (
    "A1-Peephole", "A2-Hall of Windows", "A1-PaSL", "A1-Outnumbered",
    "A1-ASooR", "A2-Guards", "A1-OtToU", "A1-Trio",
    "A2-Suicide Mission", "A3-ABTU Star", "A3-ABTU", "A3-AEP",
    "A3-Swallowed the Key", "A1-Beaten Path", "A3-Stashed for Later", "A6-Mobile Mindfield",
    "C6-Two Way Street", "B6-Egyptian Arcade", "C1-Labyrinth", "A*-DDM",
    "A*-Nervewrecker", "B7-WLJ", "A*-JfW", "B2-Higher Ground",
    "A5-Two Boxes", "A5-Two Boxes Star", "A4-Push it Further", "A4-Branch it Out",
    "A4-DCtS", "A5-Over the Fence", "A4-Above All That", "B1-WtaD",
    "A5-YKYMCTS", "B1-SaaS", "B6-JDaW", "A5-OLB",
    "B6-Crisscross", "A7-Two Buzzers", "A6-Deception", "A7-Pinhole",
    "A7-LFI", "B2-Tomb", "B*-Merry Go Round", "B4-TRA",
    "C4-Stables", "C2-Cemetery", "A6-Door too Far", "C1-Conservatory",
    "A7-WiaL", "B2-MotM", "B3-Sunshot", "B2-Moonshot",
    "B7-AFaF", "B7-BSbS Star", "C3-Three Connectors", "C6-Circumlocution",
    "C7-Prison Break", "C3-BSLS", "C7-Carrier Pigeons", "C5-Time Crawls",
    "C7-Crisscross", "C6-Seven Doors", "C*-Unreachable Garden", "B5-Plates",
    "B5-Two Jammers", "A5-FC", "A5-FC Star", "B3-Blown Away",
    "B7-BSbS", "B1-Third Wheel", "A6-Bichromatic", "A7-Trapped Inside",
    "B*-Cat's Cradle", "C7-DMS", "C5-Dumbwaiter", "B4-ABUH",
    "B5-Iron Curtain", "C1-Blowback", "C4-Armory", "B5-SES",
    "B5-Chambers", "B1-Over the Fence", "C3-Jammer Quarantine", "C3-Weathertop",
    "B1-RoD", "C*-Nexus", "B4-Double-Plate", "B4-Self Help",
    "C5-Time Flies", "B3-Eagle's Nest", "B7-BLoM", "C2-ADaaF",
    "C5-UCaJ", "C4-Oubliette Star", "C4-Oubliette", "B4-RPS",
    "C4-Throne Room", "C4-Throne Room Star", "B3-Woosh", "B*-Peekaboo",
    "B4-WAtC", "C1-MIA", "C2-Rapunzel", "C2-Short Wall",
    "C*-Cobweb", "A1-Star", "A2-Star", "A3-Clock Star",
    "A4-Star", "A6-Star", "A7-Star", "B1-Star",
    "B2-Star", "B3-Star", "B4-TRA Star", "B4-Sphinx Star",
    "B5-Obelisk Star", "B7-Star", "C1-Star", "C2-Star",
    "C3-Star", "C5-UCAJ Star", "C5-Dumbwaiter Star", "C5-Time Flies Star",
    "C6-Star", "C7-Star", "CM-Star", "F3-Star",
    "F0-Star",
    "PaintItemSeed", "Code_Floor4", "Code_Floor5", "Code_Floor6",
    "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "ADevIsland",
    "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8",
    "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "CMessenger",
    "Randomizer_Seed", "Randomizer_Mode", "Randomizer_Scavenger", "Randomizer_Loop"
)
PORTAL_ORDER = (
    "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "ADevIsland",
    "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8",
    "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "CMessenger"
)

A_MARKERS = (
    "A1-PaSL", "A1-Beaten Path", "A1-Outnumbered", "A1-OtToU", "A1-ASooR", "A1-Trio", "A1-Peephole", "A1-Star",
    "A2-Guards", "A2-Hall of Windows", "A2-Suicide Mission", "A2-Star",
    "A3-Stashed for Later", "A3-ABTU", "A3-ABTU Star", "A3-Swallowed the Key", "A3-AEP", "A3-Clock Star",
    "A4-Branch it Out", "A4-Above All That", "A4-Push it Further", "A4-Star", "A4-DCtS",
    "A5-Two Boxes", "A5-Two Boxes Star", "A5-YKYMCTS", "A5-Over the Fence", "A5-OLB", "A5-FC", "A5-FC Star",
    "A6-Mobile Mindfield", "A6-Deception", "A6-Door too Far", "A6-Bichromatic", "A6-Star",
    "A7-LFI", "A7-Trapped Inside", "A7-Two Buzzers", "A7-Star", "A7-WiaL", "A7-Pinhole"
)

TETRO_INDEXES = ["", # Used for checksum, so needs to have the same index as LUA
    "**1",      "**2",      "**3",      "**4",     "**5",
    "**6",      "**7",      "**8",      "**9",     "**10",
    "**11",     "**12",     "**13",     "**14",    "**15",
    "**16",     "**17",     "**18",     "**19",    "**20",
    "**21",     "**22",     "**23",     "**24",    "**25",
    "**26",     "**27",     "**28",     "**29",    "**30",
    "DI1",      "DI2",      "DJ1",      "DJ2",     "DJ3",
    "DJ4",      "DJ5",      "DL1",      "DL2",     "DL3",
    "DT1",      "DT2",      "DT3",      "DT4",     "DZ1",
    "DZ2",      "DZ3",      "DZ4",      "EL1",     "EL2",
    "EL3",      "EL4",      "EO1",      "ES1",     "ES2",
    "ES3",      "ES4",      "MI1",      "MJ1",     "ML1",
    "ML2",      "ML3",      "ML4",      "MO1",     "MS1",
    "MS2",      "MT1",      "MT2",      "MT3",     "MT4",
    "MT5",      "MT6",      "MT7",      "MT8",     "MT9",
    "MT10",     "MZ1",      "MZ2",      "MZ3",     "MZ4",
    "NI1",      "NI2",      "NI3",      "NI4",     "NI5",
    "NI6",      "NJ1",      "NJ2",      "NJ3",     "NJ4",
    "NL1",      "NL2",      "NL3",      "NL4",     "NL5",
    "NL6",      "NL7",      "NL8",      "NL9",     "NL10",
    "NO1",      "NO2",      "NO3",      "NO4",     "NO5",
    "NO6",      "NO7",      "NS1",      "NS2",     "NS3",
    "NS4",      "NT1",      "NT2",      "NT3",     "NT4",
    "NT5",      "NT6",      "NT7",      "NT8",     "NT9",
    "NT10",     "NT11",     "NT12",     "NZ1",     "NZ2",
    "NZ3",      "NZ4",      "NZ5",      "NZ6"
]

BACKUP_LOCKED = {
    "A1 Gate": (),
    "A Gate": ("DI1", "DJ3", "DL1", "DZ2"),
    "B Gate": (),
    "C Gate": (),
    "A Star": ("**1", "**2", "**3", "**4", "**5", "**6", "**7", "**8", "**9", "**10"),
    "B Star": ("**11", "**12", "**13", "**14", "**15", "**16", "**17", "**18", "**19", "**20"),
    "C Star": ("**21", "**22", "**23", "**24", "**25", "**26", "**27", "**28", "**29", "**30"),
    "Connector": ("ML1", "MT1", "MT2"),
    "Cube": ("ML2", "MT3", "MT4", "MZ1"),
    "Fan": ("ML3", "MS1", "MT5", "MT6", "MZ2"),
    "Recorder": ("MJ1", "MS2", "MT7", "MT8", "MZ3"),
    "Platform": ("MI1", "ML4", "MO1", "MT9", "MT10", "MZ4"),
    "F1": ("NL1", "NL2", "NZ1", "NZ2"),
    "F2": ("NL3", "NL4", "NL5", "NL6", "NO1", "NT1", "NT2", "NT3", "NT4"),
    "F3": ("NI1", "NI2", "NI3", "NI4", "NJ1", "NJ2", "NL7", "NL8", "NS1", "NZ3"),
    "F4": ("NJ3", "NL9", "NO2", "NO3", "NS2", "NS3", "NT5", "NT6", "NT7", "NT8", "NZ4", "NZ5"),
    "F5": ("NI5", "NI6", "NJ4", "NL10", "NO4", "NO5", "NO6", "NO7", "NS4", "NT9", "NT10", "NT11", "NT12", "NZ6"),
    "F6": ("EL1", "EL2", "EL3", "EL4", "EO1", "ES1", "ES2", "ES3", "ES4")
}


def rand(min, max, seed):
    seed = (214013 * seed + 2531011) % 2147483648
    if min == max:
        return min, seed
    return (seed % (max - (min - 1))) + min, seed


def checksum(talosProgress):
    talosProgress["Randomizer_Mode"] = 1
    talosProgress["Randomizer_Scavenger"] = 0
    talosProgress["Randomizer_Loop"] = 0
    talosProgress["Randomizer_ShowAll"] = 1

    sum1 = 0
    sum2 = 0
    for index in range(len(ALL_MARKERS)):
        if ALL_MARKERS[index] in talosProgress:
            value = talosProgress[ALL_MARKERS[index]]
            if isinstance(value, str):
                value = TETRO_INDEXES.index(value)
        else:
            value = -1
            print("'" + ALL_MARKERS[index] + "' does not have a value assigned to it")
        sum1 = (sum1 + value*(index + 1)) % 65536
        sum2 = (sum2 + sum1) % 65536
    return "%08X" % (sum1 * 65536 + sum2)


def check_seed(base_seed):
    talosProgress = {}

    locked = dict(BACKUP_LOCKED)
    # If I make a backup copy of this list the internal ones still point to the original
    markers = (
        (lambda: True, [
            "A1-Peephole", "A1-PaSL", "A1-Outnumbered", "A1-ASooR",
            "A1-OtToU", "A1-Trio", "A1-Beaten Path", "A1-Star"
        ]),
        (lambda: not locked["F1"] and (not locked["Connector"] or not locked["F3"]), [
            "F0-Star"
        ]),
        (lambda: not locked["F3"], [
            "F3-Star"
        ]),
        (lambda: True, [
            "A2-Hall of Windows", "A2-Guards", "A2-Suicide Mission", "A2-Star",
            "A3-ABTU Star", "A3-ABTU", "A3-AEP", "A3-Swallowed the Key",
            "A3-Stashed for Later", "A3-Clock Star",
            "A4-Push it Further", "A4-Branch it Out", "A4-Above All That", "A4-Star"
        ], "A4"),
        (lambda: not locked["Connector"], [
            "A4-DCtS"
        ], "A4"),
        (lambda: True, [
            "A5-Two Boxes", "A5-Two Boxes Star", "A5-Over the Fence", "A5-YKYMCTS",
            "A5-OLB", "A5-FC", "A5-FC Star",
            "A6-Mobile Mindfield", "A6-Deception", "A6-Door too Far", "A6-Bichromatic",
            "A6-Star",
            "A7-Two Buzzers", "A7-Pinhole", "A7-LFI", "A7-WiaL",
            "A7-Trapped Inside", "A7-Star"
        ], "A7"),
        (lambda: not (locked["A Star"] or locked["B Star"] or locked["C Star"]), [
            "A*-DDM", "A*-Nervewrecker", "A*-JfW"
        ], "A8"),
        (lambda: not locked["B Gate"], [
            "B1-SaaS", "B1-WtaD", "B1-Third Wheel", "B1-Over the Fence",
            "B1-RoD", "B1-Star",
            "B2-Higher Ground", "B2-Tomb", "B2-MotM", "B2-Moonshot",
            "B2-Star",
            "B3-Sunshot", "B3-Blown Away", "B3-Eagle's Nest", "B3-Woosh",
            "B3-Star",
            "B4-TRA", "B4-ABUH", "B4-Double-Plate", "B4-Self Help",
            "B4-RPS", "B4-WAtC", "B4-TRA Star"
        ], "B4"),
        (lambda: not locked["B Gate"] and not locked["Connector"], [
            "B4-Sphinx Star"
        ], "B4"),
        (lambda: not locked["B Gate"], [
            "B5-Plates", "B5-Two Jammers", "B5-Iron Curtain", "B5-SES",
            "B5-Chambers"
        ], "B5"),
        (lambda: not locked["B Gate"] and ((not locked["Connector"] and not locked["Fan"]) or not locked["Cube"]), [
            "B5-Obelisk Star"
        ], "B5"),
        (lambda: not locked["B Gate"], [
            "B6-Egyptian Arcade", "B6-JDaW", "B6-Crisscross",
            "B7-WLJ", "B7-AFaF", "B7-BSbS Star", "B7-BSbS",
            "B7-BLoM"
        ], "B7"),
        (lambda: not locked["B Gate"] and not locked["Fan"], [
            "B7-Star"
        ], "B7"),
        (lambda: not (locked["A Star"] or locked["B Star"] or locked["C Star"]), [
            "B*-Merry Go Round", "B*-Cat's Cradle", "B*-Peekaboo"
        ], "B8"),
        (lambda: not locked["C Gate"], [
            "C1-Labyrinth", "C1-Conservatory", "C1-Blowback", "C1-Star"
        ], "C1"),
        (lambda: not locked["C Gate"] and not locked["Cube"], [
            "C1-MIA"
        ], "C1"),
        (lambda: not locked["C Gate"], [
            "C2-Cemetery", "C2-ADaaF", "C2-Rapunzel", "C2-Short Wall",
            "C2-Star",
            "C3-Three Connectors", "C3-BSLS", "C3-Jammer Quarantine", "C3-Weathertop",
            "C3-Star",
            "C4-Stables", "C4-Armory", "C4-Oubliette Star", "C4-Oubliette",
            "C4-Throne Room Star"
        ], "C4"),
        (lambda: not locked["C Gate"] and not locked["Cube"], [
            "C4-Throne Room"
        ], "C4"),
        (lambda: not locked["C Gate"], [
            "C5-Time Crawls", "C5-Dumbwaiter", "C5-Time Flies", "C5-UCaJ",
            "C5-Time Flies Star"
        ], "C5"),
        (lambda: not locked["C Gate"] and not locked["Cube"], [
            "C5-UCAJ Star", "C5-Dumbwaiter Star"
        ], "C5"),
        (lambda: not locked["C Gate"], [
            "C6-Two Way Street", "C6-Circumlocution", "C6-Seven Doors", "C6-Star",
            "C7-Prison Break", "C7-Carrier Pigeons", "C7-Crisscross", "C7-DMS",
            "C7-Star"
        ], "C7"),
        (lambda: not (locked["A Star"] or locked["B Star"] or locked["C Star"]), [
            "C*-Nexus"
        ], "C8"),
        (lambda: not (locked["A Star"] or locked["B Star"] or locked["C Star"]) and (not locked["Connector"] or not locked["Cube"]), [
            "C*-Cobweb", "C*-Unreachable Garden"
        ], "C8"),
        (lambda: not locked["C Gate"], [
            "CM-Star"
        ], "CMessenger")
    )

    seed = base_seed
    talosProgress["Randomizer_Seed"] = seed
    talosProgress["PaintItemSeed"], seed = rand(0, 8909478, seed)
    talosProgress["Code_Floor4"], seed = rand(1, 999, seed)
    talosProgress["Code_Floor5"], seed = rand(1, 999, seed)
    codeF6 = 0
    for _ in range(3):
        digit, seed = rand(4, 9, seed)
        codeF6 = codeF6*10 + digit
    talosProgress["Code_Floor6"] = codeF6

    for index in range(len(PORTAL_ORDER)):
        name = PORTAL_ORDER[index]
        talosProgress[name] = index + 1

    checkGates = True
    allSpots = False
    placedItems = False
    placedStars = False
    availableMarkers = 0
    openMarkers = []
    closedMarkers = []
    open_worlds = []
    WorldB = []
    WorldC = []
    for i in range(len(markers)):
        if len(markers[i]) < 3:
            closedMarkers.append(i)
            continue
        markerWorld = markers[i][2]
        if markerWorld[0] == "A":
            closedMarkers.append(i)
            open_worlds.append(markers[i][2])
        elif markerWorld[0] == "B":
            WorldB.append(i)
        elif markerWorld[0] == "C":
            WorldC.append(i)
        else:
            closedMarkers.append(i)

    arranger = ""
    accessableArrangers = ["A Gate"]

    while not allSpots or len(accessableArrangers) > 0:
        toRemove = []
        for i in range(len(closedMarkers)):
            index = closedMarkers[i]
            if markers[index][0]():
                openMarkers.append(index)
                toRemove.append(i)
                availableMarkers = availableMarkers + len(markers[index][1])
        for i in range(len(toRemove)):
            closedMarkers.pop(toRemove[i] - (i - 1) - 1)

        if not allSpots:
            if (WorldB or WorldC) or (locked["A Star"] or locked["B Star"] or locked["C Star"]):
                if (WorldB or WorldC):
                    if arranger == "A Gate":
                        accessableArrangers += ["B Gate", "C Gate"]
                elif not placedStars:
                    placedStars = True
                    accessableArrangers += ["A Star", "B Star", "C Star"]
            else:
                if not placedItems:
                    placedItems = True
                    accessableArrangers += ["Connector", "Cube", "Fan", "Recorder", "Platform", "F1", "F3"]
                elif placedItems and len(closedMarkers) == 0:
                    allSpots = True
                    accessableArrangers += ["F4", "F5", "F6", "A1 Gate", "F2"]

        index, seed = rand(0, len(accessableArrangers) - 1, seed)
        arranger = accessableArrangers.pop(index)
        sigils = locked[arranger]
        locked[arranger] = None

        if checkGates:
            if arranger in ("B Gate", "C Gate"):
                chance, seed = rand(0, 99, seed)
                if chance < PROB_BOTH_HUBS:
                    sigils = ("DI2", "DL2", "DT1", "DT2", "DZ3",
                              "DJ4", "DJ5", "DL3", "DT3", "DT4", "DZ4")
                    for i in range(len(accessableArrangers)):
                        if accessableArrangers[i][2:] == "Gate":
                            accessableArrangers.pop(i)
                            break
                    locked["A1 Gate"] = ("DJ1", "DJ2", "DZ1")
                    locked["A Gate"] = None
                    locked["B Gate"] = None
                    locked["C Gate"] = None
                    for world in WorldB + WorldC:
                        closedMarkers.append(world)
                        open_worlds.append(markers[world][2])
                    WorldB = None
                    WorldC = None
                else:
                    uniqueSigils = []
                    if arranger == "B Gate":
                        uniqueSigils = ("DJ1", "DJ4", "DJ5")
                        locked["A1 Gate"] = ("DJ2", "DZ1")
                        locked["C Gate"] = ("DL3", "DT3", "DT4", "DZ4")
                        sigils = ("DI2", "DL2", "DT1", "DT2", "DZ3")
                        unlocking_world = WorldB
                        WorldB = None
                    elif arranger == "C Gate":
                        uniqueSigils = ("DI2",)
                        locked["B Gate"] = ("DL2", "DT1", "DT2", "DZ3")
                        locked["A1 Gate"] = ("DJ1", "DJ2", "DZ1")
                        sigils = ("DJ4", "DJ5", "DL3", "DT3", "DT4", "DZ4")
                        unlocking_world = WorldC
                        WorldC = None
                    for world in unlocking_world:
                        closedMarkers.append(world)
                        open_worlds.append(markers[world][2])

                    tempOpenMarkers = []
                    tempAvailableMarkers = 0
                    for index in closedMarkers:
                        if markers[index][0]():
                            tempOpenMarkers.append(index)
                            tempAvailableMarkers = tempAvailableMarkers + len(markers[index][1])

                    for i in uniqueSigils:
                        index, seed = rand(0, tempAvailableMarkers - 1, seed)
                        for tempOpenMarker in tempOpenMarkers:
                            if index >= len(markers[tempOpenMarker][1]):
                                index = index - len(markers[tempOpenMarker][1])
                            else:
                                randMarker = markers[tempOpenMarker][1].pop(index)
                                talosProgress[randMarker] = i
                                tempAvailableMarkers -= 1
                                break
                checkGates = False
        elif not checkGates:
            if arranger == "B Gate":
                for world in WorldB:
                    closedMarkers.append(world)
                    open_worlds.append(markers[world][2])
                WorldB = None
            elif arranger == "C Gate":
                for world in WorldC:
                    closedMarkers.append(world)
                    open_worlds.append(markers[world][2])
                WorldC = None

        for i in sigils:
            index, seed = rand(0, availableMarkers - 1, seed)
            for openMarker in openMarkers:
                if index >= len(markers[openMarker][1]):
                    index = index - len(markers[openMarker][1])
                else:
                    randMarker = markers[openMarker][1].pop(index)
                    if i[0] == "E" and (randMarker[0] != "A" or randMarker[1] == "*"):
                        return False
                    talosProgress[randMarker] = i
                    availableMarkers -= 1
                    if len(markers[openMarker][1]) == 0:
                        openMarkers.remove(openMarker)
                    break

    l_count = 0
    z_count = 0
    for marker in A_MARKERS:
        sigil = talosProgress[marker]
        if sigil[0] == "N":
            if sigil[1] == "L":
                l_count += 1
            if sigil[1] == "Z":
                z_count += 1
    if l_count >= 2 and z_count >= 2:
        output = "{}, {}, {}".format(base_seed, checksum(talosProgress), talosProgress["Code_Floor6"])
        print(output)
        with open("output.txt", "a") as file:
            file.write(output + "\n")
        return True


def init_worker():
    # Ignore SIGINT (Control-C) for children
    signal.signal(signal.SIGINT, signal.SIG_IGN)


if __name__ == "__main__":
    start_seed = 0
    max_seed = 0x7FFFFFFF
    if len(sys.argv) > 1:
        start_seed = int(sys.argv[1])
    if len(sys.argv) > 2:
        max_seed = max(start_seed, min(0x7FFFFFFF, int(sys.argv[2])))

    pool = multiprocessing.Pool(8, init_worker)
    for base_seed in range(start_seed, max_seed+1, 1000):
        try:
            pool.map(check_seed, range(base_seed, base_seed+1000))
        except KeyboardInterrupt:
            pool.terminate()
            pool.join()
            print("Stopped while working on", base_seed, "through", base_seed+1000)
        except ValueError:
            break  # Thrown during shutdown
