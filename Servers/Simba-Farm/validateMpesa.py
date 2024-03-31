def validateNumber(phone_no):
    state = False
    print("Number length = %s"%(len(phone_no)))
    if len(str(phone_no)) > 8:
        if len(str(phone_no)) == 9 or len(str(phone_no)) == 11:
            state = True
        else:
            state = False
        print(str(phone_no)[0]+str(phone_no)[1])
        print(str(phone_no)[0]+str(phone_no)[1]+str(phone_no)[2])
        if (str(phone_no)[0]+str(phone_no)[1]) == "07" or (str(phone_no)[0]+str(phone_no)[1]) == "01" or (str(phone_no)[0]+str(phone_no)[1]+str(phone_no)[2]) == "254":
            state = True
        else:
            state = False

    return state