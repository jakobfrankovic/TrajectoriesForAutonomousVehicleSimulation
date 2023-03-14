import pandas as pd
import math 

pd.set_option('display.max_rows', None)

def checkerFCFS(arrivalTime1, arrivalTime2):

    d = {'lane': [], 'arrival': [], 'departure': []}
    df = pd.DataFrame(data=d)

    lane = 0
    lastDepartureTime = 0
    result = []

    if arrivalTime1[0] < arrivalTime2[0]:
        lastDepartureTime = arrivalTime1.pop(0)
    else:
        lane = 1
        lastDepartureTime = arrivalTime2.pop(0)

    new_row = [lane, lastDepartureTime, lastDepartureTime]
    df.loc[len(df)] = new_row

    result.append(lastDepartureTime)

    while len(arrivalTime1) != 0 or len(arrivalTime2) != 0:
        if len(arrivalTime1) == 0:
            arrivalTime = arrivalTime2.pop(0)
            if lane == 0:
                lastDepartureTime += 2.4
                result.append(lastDepartureTime)
                lane = 1
            else:
                lastDepartureTime += 1
                result.append(lastDepartureTime)
        elif len(arrivalTime2) == 0:
            arrivalTime = arrivalTime1.pop(0)
            if lane == 0:
                lastDepartureTime += 1
                result.append(lastDepartureTime)
            else:
                lastDepartureTime += 2.4
                result.append(lastDepartureTime)
                lane = 0
        else:
            if arrivalTime1[0] < arrivalTime2[0]:
                arrivalTime = arrivalTime1.pop(0)
                if lane == 0:
                    lastDepartureTime += 1
                    result.append(lastDepartureTime)
                else:
                    lastDepartureTime += 2.4
                    result.append(lastDepartureTime)
                    lane = 0
            else:
                arrivalTime = arrivalTime2.pop(0)
                if lane == 0:
                    lastDepartureTime += 2.4
                    result.append(lastDepartureTime)
                    lane = 1
                else:
                    lastDepartureTime += 1
                    result.append(lastDepartureTime)

        new_row = [lane, arrivalTime, lastDepartureTime]
        df.loc[len(df)] = new_row
    
    # print(df)
    # print(result)
    return result 

def checkerExhaustive(arrivalTime1, arrivalTime2):

    d = {'lane': [], 'arrival': [], 'departure': []}
    df = pd.DataFrame(data=d)

    lane = 0
    lastDepartureTime = 0
    result = []
    lane0arrival = []
    lane1arrival = []

    if arrivalTime1[0] < arrivalTime2[0]:
        lastDepartureTime = arrivalTime1.pop(0)
        lane0arrival.append(lastDepartureTime)
    else:
        lane = 1
        lastDepartureTime = arrivalTime2.pop(0)
        lane1arrival.append(lastDepartureTime)

    new_row = [lane, lastDepartureTime, lastDepartureTime]
    df.loc[len(df)] = new_row

    result.append(lastDepartureTime)

    while len(arrivalTime1) != 0 or len(arrivalTime2) != 0:
        if len(arrivalTime1) == 0:
            arrivalTime = arrivalTime2.pop(0)
            if lane == 0:
                lastDepartureTime += 2.4
                result.append(lastDepartureTime)
                lane1arrival.append(lastDepartureTime)
                lane = 1
            else:
                lastDepartureTime += 1
                lane1arrival.append(lastDepartureTime)
                result.append(lastDepartureTime)
        elif len(arrivalTime2) == 0:
            arrivalTime = arrivalTime1.pop(0)
            if lane == 0:
                lastDepartureTime += 1
                result.append(lastDepartureTime)
                lane0arrival.append(lastDepartureTime)
            else:
                lastDepartureTime += 2.4
                result.append(lastDepartureTime)
                lane0arrival.append(lastDepartureTime)
                lane = 0
        else:
            if lane == 0:
                arrivalTime = arrivalTime1[0]
                if round(arrivalTime - lastDepartureTime, 4) > 1:
                    if arrivalTime1[0] > arrivalTime2[0]:
                        lastDepartureTime += 2.4
                        result.append(lastDepartureTime)
                        arrivalTime = arrivalTime2.pop(0)
                        lane1arrival.append(lastDepartureTime)
                        lane = 1
                    else:
                        lastDepartureTime = arrivalTime1[0]
                        result.append(lastDepartureTime)
                        lane0arrival.append(lastDepartureTime)
                        arrivalTime = arrivalTime1.pop(0)
                else:
                    lastDepartureTime += 1
                    result.append(lastDepartureTime)
                    lane0arrival.append(lastDepartureTime)
                    arrivalTime = arrivalTime1.pop(0)
            else:
                arrivalTime = arrivalTime2[0]
                if round(arrivalTime - lastDepartureTime, 4) > 1:
                    if arrivalTime2[0] > arrivalTime1[0]:
                        lastDepartureTime += 2.4
                        result.append(lastDepartureTime)
                        lane0arrival.append(lastDepartureTime)
                        arrivalTime = arrivalTime1.pop(0)
                        lane = 0
                    else:
                        lastDepartureTime = arrivalTime2[0]
                        result.append(lastDepartureTime)
                        lane1arrival.append(lastDepartureTime)
                        arrivalTime = arrivalTime2.pop(0)
                else:
                    lastDepartureTime += 1
                    result.append(lastDepartureTime)
                    lane1arrival.append(lastDepartureTime)
                    arrivalTime = arrivalTime2.pop(0)

        new_row = [lane, arrivalTime, lastDepartureTime]
        df.loc[len(df)] = new_row
    
    print(df)
    # print(result)
    # print(lane0arrival)
    # print(lane1arrival)
    return result, lane0arrival, lane1arrival

# dataframe = pd.read_excel('arrivals30.xlsx', header=None)
dataframe = pd.read_excel('sampleoutput.xlsx', header=None)

arrivalTime1 = dataframe[dataframe.columns[0]].to_list()
arrivalTime2 = dataframe[dataframe.columns[1]].to_list()


arrivalTime1 = [x for x in arrivalTime1 if str(x) != 'nan']
arrivalTime2 = [x for x in arrivalTime2 if str(x) != 'nan']

arrivalTime1 = arrivalTime1[:50]
arrivalTime2 = arrivalTime2[:50]

arrivalTime1 = [1, 2, 4.816, 9.158]
arrivalTime2 = [2.309, 3.309, 5.169, 6.985, 8.051, 9.996]

result, lane0arrival, lane1arrival = checkerExhaustive(arrivalTime1, arrivalTime2)
print(lane0arrival)




