from firscheck import timed_timer
import datetime
import dill as pickle
import sys
# self.time_delta_ob_duration
# self.start_time
# def handel_calling(self,print_thread,per_iteration_time,available_total_time)


def pickled_items(filename):
    """ Unpickle a file of pickled data. """
    try:
        with open(filename, "rb") as f:
            while True:
                try:
                    yield pickle.load(f)
                except EOFError:
                    break
    except FileNotFoundError:
        return -1


def write_items(filename, diction):
    with open(filename, "wb") as f:
        for i in diction:
            pickle.dump(i, f)


def main():
    one_time_load = 1
    print("-------------------Alarmy-------------------")
    quit = False
    alarms_exist = False
    while not quit:
        change = False
        list_queue = []
        print("Loading Alarms..")
        for i in pickled_items("alarms.pickle"):
            if(i == -1):
                print("No alarm exists")
                alarms_exist = False
            list_queue.append(i)
            alarms_exist = True

# logic to sort and check alarms start time as per start time
        while(alarms_exist):
            for i in list_queue:  # remove un wantedd items
                if(not i.start_time or i.end):
                    list_queue.remove(i)
                    print("removed ", i)
                    change = True
            if(len(list_queue) == 0):
                alarms_exist = False
                break
                # break through multiple if statement
            list_queue = sorted(
                list_queue, key=lambda timed_timer: timed_timer.start_time)
            # if(one_time_load):
            for i in list_queue:  # calling their respective threads
                if(not i.end):
                    returned = i.handel_time(i.start_time)
                    if(returned[0] == -1):
                        print(f"Removed Alarms with {i.start_time}")
                        list_queue.remove(i)
                        change = True
                        continue
                    print(i.main_call_with_timer.is_alive())
                    diff = returned[2]
                    # one time functions
                    if (i.running is False and i.running_cron is False) or ((diff + i.time_delta_ob_duration).total_seconds() > 0):
                        total_time = i.time_delta_ob_duration.total_seconds()
                        print(total_time, i.time_delta_ob_duration)
                        available_total_time = total_time
                        i.timer_time = diff.total_seconds() if i.mode_future else i.timer_time
                        per_iteration_time = available_total_time / i.no_of_iteration
                        print("timer time", i.timer_time, available_total_time)
                        i.handel_calling(
                            available_total_time, per_iteration_time)
            break
            # one_time_load -= 1
        print(list_queue)
        for i in list_queue:
            print(f"{i.start_time} {i.time_delta_ob_duration} ")
        print("Please Select")
        inp = input("1.Add Alarms 2.Edit Alarms 3.Settings 4.Quit").strip()
        if(inp == "1"):
            print("You may enter exit to be back to main menu")
            # try:
            new_obj = timed_timer()
            ret = new_obj.claculate()
            if(ret == 0):
                print("succesfully Scheduled ")
                list_queue.append(new_obj)
                change = True
            else:
                print("unsuccesfull to Schedule ")
            # except Exception as e:
            #     print("something went wrong ", e)
            pass
        elif(inp == "2"):
            if(len(list_queue) != 0):
                new_list = [[i + 1, str(list_queue[i].start_time), str(list_queue[i].time_delta_ob_duration.total_seconds(
                )), str(list_queue[i].no_of_iteration)] for i in range(len(list_queue))]
                new_list = [["S.no", "Start time",
                             "total_seconds", "no of iteration"]] + new_list
                width_list = [[], [], []]
                for x in range(len(new_list)):
                    width_list[0].append(len(new_list[x][1]))
                    width_list[1].append(
                        len(new_list[x][2]))
                    width_list[2].append(len(new_list[x][3]))
                width_col1 = max(len(list_queue) - 1, 4)
                width_col2 = max(width_list[0])
                width_col3 = max(width_list[1])
                width_col4 = max(width_list[2])
                for i in range(len(new_list)):
                    print(f"| {new_list[i][0]:<{width_col1}} | {new_list[i][1]:<{width_col2}} | {new_list[i][2]:<{width_col3}} | {new_list[i][3]:<{width_col4}} | ")
                while True:
                    try:
                        no = int(input("Choose alarm"))
                        list_queue[no - 1].end = True
                        change = True
                        break
                    except:
                        print("Try again!")
            else:
                print("No Alarms to show")
            pass
        elif(inp == "3"):
            pass
        elif(inp == "4"):
            break
        else:
            print("Invalid Entry,")
            continue
        # write only if there is change
        if(change):
            write_items("alarms.pickle", list_queue)

    sys.exit()


if __name__ == '__main__':
    main()
