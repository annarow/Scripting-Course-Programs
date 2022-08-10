#Anna Rowena Waldron

#main function which calls all other functions.
def main():
    print("insert baseline file:")
    file_base = input()
    print("insert test file:")
    file_test = input()
    btl, bec, btc = read_file(file_base)#base taken list, base empty cookie, base taken cookie
    ttl, tec, ttc = read_file(file_test)    #test taken list, test empty cookie, test taken cookie
    bsd,total_segments = handle_segments(btl)  #base segment dictionar
    bcd = handle_cookies(btl) #base cookie dictionary
    tsd, total_segments1 = handle_segments(ttl)  #test segment dictionary
    tcd = handle_cookies(ttl)   #test cookie dictionary
    base_full_only, test_full_only, both_full, either_full = check_empties(btl, ttl, bec, tec)
    first_report(btl, bec, btc, ttl, tec, ttc, base_full_only, test_full_only, both_full, either_full)
    turn = 0
    added_cookies_seg, removed_cookies_seg, added, removed = compare_segments(bsd, tsd, turn) #segments dict used
    turn = 1
    add_seg, remove_seg, add_c, remove_c = compare_segments(bcd, tcd, turn)   #cookies dict used
    second_report(added_cookies_seg, removed_cookies_seg, added, removed, add_seg, remove_seg, add_c, remove_c, btc, total_segments)

#function that opens and reads the file and splits up each lines into a list.
def read_file(files):
    empty_cookies = []
    taken_cookies = []
    with open(files) as file:
        for line in file:
            if "evaluated: " not in line:
                continue  
            first_split = line.strip().split("evaluated: ")
            second_split = first_split[1]
            second_split = second_split.split(" ==> ")
            second_split[1] = second_split[1].strip("[").strip("]")
            if len(second_split[1]) == 0 :
                second_split.pop()
                empty_cookies.append(second_split)
            else:
                taken_cookies.append(second_split)
    total_cookies = len(empty_cookies)+len(taken_cookies)
    taken_cookies.sort()
    print(taken_cookies)
    return taken_cookies, empty_cookies, total_cookies

#checks for information about non-empty cookies in baseline only, non-empty cookies in test only,non-empty cookies in both,
# and non-empty cookies in either. Returns integers about this information in 4 seperate variables.
def check_empties(btl, ttl, bec, tec): #baseline taken list, test taken list
    base_full_only = 0
    test_full_only = 0
    both_full = 0
    for i in range(len(btl)):
        for j in range(len(ttl)):
            if btl[i][0] == ttl[j][0]:
               both_full += 1
    base_full_only = len(btl) - both_full
    test_full_only = len(ttl) - both_full
    either_full = base_full_only + test_full_only
    print(base_full_only)
    print(test_full_only)
    print(both_full)
    return base_full_only, test_full_only, both_full, either_full      

#function that creates a dictionary keyed by segments and valued by a list of cookies. Returns dictionary and
#the total count of segments.
def handle_segments(taken_list):
    segment_dict = {}
    total_segments = 0
    for i in range(len(taken_list)):
        working = taken_list[i].pop()
        working = working[1:]
        working = working.split(", ")
        taken_list[i].append(working)
    for j in range(len(taken_list)):
        for m in range(1, len(taken_list[j])):
            for n in range(len(taken_list[j][m])):
                if taken_list[j][m][n] not in segment_dict:
                    segment_dict[taken_list[j][m][n]] = []
                    total_segments += 1
                if taken_list[j][m][n] in segment_dict:
                    segment_dict[taken_list[j][m][n]].append(taken_list[j][0])
    print(segment_dict)
    total_segments = len(segment_dict)
    return segment_dict, total_segments    

def handle_cookies(taken_list):
    cookie_dict = {}
    for i in range(len(taken_list)):
        cookie_dict[taken_list[i][0]] = taken_list[i][1]
    return cookie_dict

#function that is used to compare the segments and cookies and creates new dictionaries for the segments with added
#cookies and a dictionary of removed cookies. Returns these dictionaries and the count of removed and added.
def compare_segments(base_segment_dict, test_segment_dict, turn):
    added_cookies_seg = {}
    added = 0
    removed = 0
    removed_cookies_seg = {}
    for tKey, tValue in test_segment_dict.items():
        if tKey in base_segment_dict:
            for i in range(len(tValue)):
                if tValue[i] not in base_segment_dict[tKey]:
                    if turn == 0:
                        added += 1
                        added_cookies_seg[tKey] = tValue
                    else:
                        turn == 1
                        added += 1
                        added_cookies_seg[tKey] = tValue
                        break
    for bKey, bValue in base_segment_dict.items():
        if bKey in test_segment_dict:
            for j in range(len(bValue)):
                if bValue[j] not in test_segment_dict[bKey]:
                    removed += 1
                    removed_cookies_seg[bKey] = bValue
        elif bKey not in test_segment_dict:
            removed += 1
            removed_cookies_seg[bKey] = bValue
    return added_cookies_seg, removed_cookies_seg, added, removed

#function which creates a file and writes to it the first part of the summary   
def first_report(btl, bec, btc, ttl, tec, ttc, base_full_only, test_full_only, both_full, either_full):
    w = open("newreport.txt", "w+")
    w.write("Summary:\n")
    w.write("total cookies in baseline =     %s\n" %(btc))
    w.write("empty cookies in baseline =    %s\n" %(len(bec)))
    w.write("non-empty cookies in baseline =    %s\n" %(len(btl)))
    w.write("total cookies in test =     %s\n" %(ttc))
    w.write("empty cookies in test =    %s\n" %(len(tec)))
    w.write("non-empty cookies in test =    %s\n" %(len(ttl)))
    w.write("non-empty cookies in baseline only =	    %s\n" %(base_full_only))
    w.write("non-empty cookies in test only =	%s\n" %(test_full_only))
    w.write("non-empty cookies in both =	  %s\n" %(both_full))
    w.write("non-empty cookies in either =      %s\n" %(either_full))
    print("non-empty cookies in baseline only =	    ",base_full_only)

#function which opens and appends to the file created above and finishes the report
def second_report(added_cookies_seg, removed_cookies_seg, added, removed, add_seg, remove_seg, add_c, remove_c, btc, total_segs):
    w = open("newreport.txt", "a+")
    counts = 0
    w.write("Segments with added cookies:   %s / %s\n" %(added, total_segs))
    for key, value in added_cookies_seg.items():
        amount = len(value)
        w.write("%s    %s    %s    %s\n" %(counts, key, amount, value))
        counts += 1    
    count2 = 0
    w.write("Segments with removed cookies:   %s / %s\n" %(removed, total_segs))
    for sKey, sValue in removed_cookies_seg.items():
        amount2 = len(sValue)
        w.write("%s    %s    %s    %s\n" %(count2, sKey, amount2, sValue))
        count2 += 1
    count3 = 0
    w.write("Cookies in extra segments:    %s / %s\n" %(add_c, btc))
    for ckey, cvalue in add_seg.items():
        amount3 = len(cvalue)
        w.write("%s    %s    %s    %s\n" %(count3, ckey, amount3, cvalue))
        count3 += 1
    count4 = 0
    w.write("Cookies omitted from segments:   %s / %s\n" %(remove_c, btc))
    for cKey, cValue in remove_seg.items():
        amount4 = len(cValue)
        w.write("%s    %s    %s    %s\n" %(count4, cKey, amount4, cValue))
        count4 += 1
    
main()
