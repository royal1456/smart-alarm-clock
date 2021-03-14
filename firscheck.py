import pyttsx3
import time
from collections import OrderedDict
import datetime
import pytz
from tzlocal import get_localzone
import threading
import concurrent.futures
from inputimeout import inputimeout, TimeoutOccurred
import queue
sys_local = get_localzone()  # pytz compatible time zone is retutned

# uncomment lines below pass for debug mode
#------------search-functions------


class timed_timer():
    def onWord(self, name, location, length):
        if self.skip or not self.running or self.next_c:
            self.engine.stop()

    def processor(self):
        while self.running and self.running_cron:
            try:
                # print("speak in")
                job = self.queue.get()
                # print("speak out")
                self.engine.say(job)
                self.engine.runAndWait()
                # print("speak out")
            except:
                # print("No pending tasks to speak")
                time.sleep(self.reaction_time)
        # print("Exited this queue")

    def non_block_run(self, prompt):
        self.queue.put(prompt)
        if(self.queue_thread.is_alive() is not True):
            self.queue_thread = threading.Thread(target=self.processor)
            self.queue_thread.start()

    def inp_time(prompt):
        while True:
            entered_time = input(prompt).strip()

            if(entered_time == "" or entered_time == None):
                return -1  # none entry
            elif(entered_time == "exit"):
                return entered_time
            # 24 hh:mm:ss
            # entered_time = '02:30:00'
            list_time = list(map(int, entered_time.split(':')))
            if(len(list_time) != 3):
                print("Illegal entry! Try again")
                continue

            try:
                if (list_time[0] > -1) and (list_time[0] < 25):
                    if (list_time[1] > -1) and (list_time[1] < 60):
                        if (list_time[2] > -1) and (list_time[2] < 60):
                            break
                        else:
                            print("Invalid seconds")
                    else:
                        print("Invalid minutes")
                else:
                    print("Invalid hours")
            except:  # for invalid strings
                print("Sorry, INVALID Time")
        return list_time

    def GetTimeZoneName(timezone, country_code):

        # see if it's already a valid time zone name
        if timezone in pytz.all_timezones:
            return timezone

        # if it's a number value, then use the Etc/GMT code
        try:
            offset = int(timezone)
            if offset > 0:
                offset = '+' + str(offset)
            else:
                offset = str(offset)
            return 'Etc/GMT' + offset
        except ValueError:
            pass

        # look up the abbreviation
        country_tzones = None
        try:
            country_tzones = pytz.country_timezones[country_code]
        except:
            pass
        set_zones = set()
        if country_tzones is not None and len(country_tzones) > 0:
            for name in country_tzones:
                tzone = pytz.timezone(name)
                for utcoffset, dstoffset, tzabbrev in getattr(tzone, '_transition_info', [[None, None, datetime.datetime.now(tzone).tzname()]]):
                    if tzabbrev.upper() == timezone.upper():
                        set_zones.add(name)
            if len(set_zones) > 0:
                return min(set_zones, key=len)

            # none matched, at least pick one in the right country
            return min(country_tzones, key=len)

        # invalid country, just try to match the timezone abbreviation to any time zone
        for name in pytz.all_timezones:
            tzone = pytz.timezone(name)
            for utcoffset, dstoffset, tzabbrev in getattr(tzone, '_transition_info', [[None, None, datetime.datetime.now(tzone).tzname()]]):
                if tzabbrev.upper() == timezone.upper():
                    set_zones.add(name)

        if len(set_zones) > 0:
            return min(set_zones, key=len)
        return "-1"

    #------------Threads--------------
    def handel_calling(self, per_iteration_time, available_total_time):
        if(self.timer_time == 0 or self.mode_future):
            self.main_call_with_timer = threading.Timer(self.timer_time, self.run_threads, [
                per_iteration_time, available_total_time, self.no_of_iteration])
            self.main_call_with_timer.start()
            print("waiting ")
        else:
            self.my_iterative_call(self.run_threads, [
                per_iteration_time, available_total_time, self.no_of_iteration])

    def my_iterative_call(self, func, argss):
        # original task to be scheuled
        while self.main_call_with_timer.is_alive():
            time.sleep(reaction_time)
        self.running_cron = True
        self.main_call_with_timer = threading.Timer(0, func, args=argss)
        self.main_call_with_timer.start()
        threading.Timer(self.timer_time, self.my_iterative_call,
                        args=[func, argss]).start()

    def empty_thread():
        pass

    def __init__(self):
        self.mode_future = False
        self.skip = False
        self.next_c = False
        self.running = True
        self.enetred_in_io = True
        self.read_inp = True
        self.reaction_time = 1
        self.engine = None  # made wheneever necesary
        self.queue = queue.Queue()
        self.running_cron = True
        self.end = False
        # -----------Input-Valus-----------
        # entered_duration = '00:10:00'
        self.queue_thread = threading.Thread(target=self.processor)
        self.no_of_iteration = 4
        self.rate_value = 175
        self.words = 100
        self.events = OrderedDict({"Think Phase": 0.1, "Make Test Case": .2,
                                   "write Approach": .3, "Implement Phase": .4})  # percantages
        # # yyy-mm-dd
        # entered_date = '2020-04-19'
        # input('Enter Time Of commencing: in HH:MM:SS')
        # # 24 hh:mm:ss
        # entered_time = '02:30:00'
        self.standard_time = 5
        self.notification_after = 1 / 3  # of total time left
        self.start_time = 0
        self.time_delta_ob_duration = datetime.timedelta(
            days=0, hours=0, minutes=0, seconds=0)
        self.main_call_with_timer = threading.Thread(
            target=timed_timer.empty_thread)
    # every stop is handeled internally in sleep and speaking so in next iteration its just changed in threads loop()

    def sleep(self, t):
        count = 0
        # global skip, next_c, start,reaction_time
        self.reaction_time = int(self.reaction_time)
        tc = t
        print(tc)
        while(not self.skip and not self.next_c and self.running and int(t) > 0):
            time.sleep(self.reaction_time)
            t -= self.reaction_time
            count += self.reaction_time
        print("got in sleep", count, int(tc))
        if(count != int(tc)):
            return -1
        else:
            return 0

    def print_speak(self, per_iteration_time):
            # global skip, next_c, start,read_inp
        while(True):
            if(self.running):
                for values in self.events:
                    if(self.next_c or not self.running):
                        break
                    if(self.skip):
                        self.skip = False
                    print(values, self.events[values])
                    alloted_time = per_iteration_time * self.events[values]
                    print(f"we got {alloted_time}")
                    notify_before = self.notification_after * alloted_time
                    self.non_block_run(f"Coming,up next {values} in")
                    if(self.reaction_time < notify_before):
                        for i in range(self.standard_time, 0, -1):
                            self.non_block_run(f'{i} ')
                        # self.engine.runAndWait()
                        # time_left_until_pop_up
                        if(self.sleep(alloted_time - notify_before) != 0):
                            continue
                        print("notify")
                        self.non_block_run("pop-pop")
                        if(self.sleep(notify_before) != 0):  # complete total time
                            continue  # continue and handel in case any flag is changed
                    else:
                        self.non_block_run("skipping ahead,very less time")
                self.read_inp = False
                print("Thrown out,must be called")
                return  # support first break stateement

            else:
                print("thread not started yet")
                time.sleep(self.reaction_time)

        # return -1

    def listen(self):
        # global skip, next_c, start,read_inp
        while self.read_inp:
            print(self.read_inp, " was")
            enterd = None
            try:
                enterd = inputimeout(prompt='>>', timeout=5)
            except TimeoutOccurred:
                pass
                # print('something-timeout')
            if(self.read_inp):
                pass
                # print("entered value", enterd, type(enterd))
            if(enterd == 'skip' or enterd == '/s'):
                self.non_block_run("skipping event")
                self.skip = True
            if(enterd == 'next' or enterd == '/n'):
                self.non_block_run("next iteration")
                self.next_c = True
                return True
            if(enterd == 'enter' or enterd == ''):
                self.running = True
            if (enterd == 'quit' or enterd == '/q'):
                self.non_block_run("quitting")
                self.running = False
                return False
            if (enterd == None):
                pass
                # print("checked none")
        # if read input has been revocked
        print("revokedd inp")
        return True

    def run_threads(self, per_iteration_time, available_total_time, no_of_iteration):
        self.engine = pyttsx3.init()
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', self.rate_value)
        self.engine.connect('started-word', self.onWord)
        # global skip, next_c, start, reaction_time,enetred_in_io,read_inp
        diff = 0
        print_thread = threading.Thread(
            target=self.print_speak, args=[per_iteration_time])
        with concurrent.futures.ThreadPoolExecutor() as executor:
            while (self.enetred_in_io and no_of_iteration > 0):
                start_t = time.time()
                available_total_time -= diff
                print(f"this ran in {diff} despite {per_iteration_time}")
                per_iteration_time = available_total_time / no_of_iteration
                print(f"nxt time is {per_iteration_time}")
                if(per_iteration_time < 0):
                    self.non_block_run(f"Overloaded Quiting")
                    self.running = False

                print(no_of_iteration, "   ", print_thread.is_alive())
                # conditional check for ruunning thread thread first time
                if (print_thread.is_alive() is not True):
                    print("entered thread")
                    pass
                else:
                    print_thread.join()
                    # while(print_thread.is_alive() is not True):# to make new thread for next phase and wait until previous rerturns
                    print("thread made in while loop")
                self.read_inp = True
                self.next_c = False
                self.running = True
                self.skip = False
                print_thread = threading.Thread(
                    target=self.print_speak, args=[per_iteration_time])
                print_thread.start()
                print("excutor called")
                # future_print = executor.submit(print_speak)
                future = executor.submit(self.listen)
                # return_speak = future_print.result()
                self.enetred_in_io = future.result()
                print("returned io ", self.enetred_in_io)
                diff = time.time() - start_t
                no_of_iteration -= 1
                # if(return_speak == -1):
                #     enetred_in_io = False
                #     break
            if(not self.running_cron):
                self.end = True
            print("exited_run")
            print_thread.join()
            self.running = False  # automatically stopks queue therad
            self.running_cron = False
            if(self.queue_thread.is_alive):
                print("Waiting for speaking to end")
                self.queue_thread.join()
            print("exited_confirmed")
    #---------------Calculation-------------

    def handel_time(self, datetime_entered_unaware):
        try:
            datetime_entered_aware = pytz.timezone(
                self.t_zone).localize(datetime_entered_unaware)
        except ValueError:
            datetime_entered_aware = datetime_entered_unaware
            # may be future timezone time is already set
        datetime_local_unaware = datetime.datetime.now()
        datetime_local_aware = sys_local.localize(
            datetime_local_unaware)
        print("time being")
        print(datetime_local_aware)
        print(datetime_entered_aware)
        diff = datetime_entered_aware - datetime_local_aware
        # print("diff is", diff, diff.total_seconds(),self.time_delta_ob_duration)
        if(datetime_entered_aware + self.time_delta_ob_duration < datetime_local_aware):
            print("Alarm time already expired (past event) ",
                  datetime_local_aware + diff, "\nas per " + str(sys_local))  # reenter date adn time
            return [-1]
        else:
            print("Alarms scheduled, will start at ",
                  datetime_local_aware + diff, "\n-as per " + str(sys_local))
            return [0, datetime_entered_aware, diff]

    def claculate(self):
        self.timer_time = [0, 0, 0]  # deafult timer
        c = input("""if u wish to start Timer now (or to run as cron) press enter key or to
            enter time manually press any other key""")
        if(c == "" or c == None):
            inp_v = timed_timer.inp_time(
                "Enter Cron interval at which u would like to run or to skip press enter")
            if(inp_v != -1):
                self.timer_time = inp_v
                datetime_local_unaware = datetime.datetime.now()
                datetime_local_aware = sys_local.localize(
                    datetime_local_unaware)
                self.start_time = datetime_local_aware  # saving time to be handeled later
            elif(inp_v == "exit"):
                return -1
        elif(c == "exit"):
            return -1

        else:
            while True:  # for try catch until final object creation
                while True:
                    entered_date = input("""Enter Date Of commencing (in yyyy.mm.dd)
                    please consider time zone while writing: """).strip()  # yyy-mm-dd
                    if(entered_date == "exit"):
                        return -1
                    # entered_date = '2020-04-19'
                    list_date = list(map(int, entered_date.split('.')))
                    if(len(list_date) != 3):
                        print("Illegal entry! Try again")
                        continue
                    try:
                        if (list_date[0] > 0):
                            if (list_date[1] > 0) and (list_date[1] < 13):
                                if (list_date[2] > 0) and (list_date[2] < 32):
                                    break  # first while break
                                else:
                                    print("Invalid days")
                            else:
                                print("Invalid months")
                        else:
                            print("Invalid year")
                    except:  # for invalid strings
                        print("Sorry, INVALID date")

                list_time = timed_timer.inp_time(
                    'Enter Time Of commencing: in HH:MM:SS ')
                if(list_time == "exit"):
                    return -1

                while True:
                    # gets string futher convert to time zone object
                    print("Enter timezones Olson timezones are used ")
                    print(
                        "Enter abbreviation used if unsure, to skip press enter and enter country code ")
                    abb = input()
                    if(abb == None or abb == ""):
                        abb = "XXX"
                        break
                    elif(len(abb) == 3):
                        break
                    elif(abb == "exit"):
                        return -1
                    else:
                        print("please ensure timezone is of maximum 3 length ")
                while True:
                    countrty_code = input(
                        "Enter 2 alphabet country code (may skip for timezones like utc..)")
                    if (countrty_code == None or countrty_code == ""):
                        countrty_code = "XX"
                    elif(countrty_code == "exit"):
                        return -1
                    self.t_zone = timed_timer.GetTimeZoneName(
                        abb, countrty_code)
                    if(self.t_zone == '-1'):
                        print("No time zones found please skip")
                        continue
                    else:
                        break
                    print(self.t_zone)
                try:
                    datetime_entered_unaware = datetime.datetime(*list_date, *list_time)
                except:
                    print(
                        "something went wrong please check dates and time with leap year and other mistakes")
                    continue
                returned = self.handel_time(datetime_entered_unaware)
                if(returned[0] != 0):
                    return -1
                datetime_entered_aware = returned[1]
                diff = returned[2]
                self.start_time = datetime_entered_aware
                self.mode_future = True
                self.timer_time = list(map(float, str(diff).split(':')))
                break
        avg_time = [3600, 60, 1]
        self.timer_time = [self.timer_time[i] * avg_time[i] for i in range(3)]
        print(self.timer_time)
        self.timer_time = sum(self.timer_time)
        while True:
            days_entered = int(input("Enter No. of days in duration :"))
            if(days_entered > -1):
                break
            elif(days_entered == "exit"):
                return -1
            print("Sorry, INVALID date")
        while True:
            converted_dur = timed_timer.inp_time(
                'Enter Duration In Total(of event)(HH:MM:SS):')
            if(converted_dur == "exit"):
                return -1
            if(self.timer_time != 0 and not self.mode_future):
                if(sum([converted_dur[i] * avg_time[i] for i in range(3)]) >= self.timer_time):
                    print(f"duration should be less than cron job {self.timer_time}seconds")
                    continue
            break
        # entered_duration = '00:10:00'
        self.time_delta_ob_duration = datetime.timedelta(
            days=days_entered, hours=converted_dur[0], minutes=converted_dur[1], seconds=converted_dur[2])
        # subtracting a min for time taken to speak all those words rate==175,words pm
        total_time = self.time_delta_ob_duration.total_seconds()
        print(total_time, self.time_delta_ob_duration)
        available_total_time = total_time
        per_iteration_time = available_total_time / self.no_of_iteration
        print(per_iteration_time)
        # 0s seconds at start

        # voices = self.engine.getProperty('voices')
        # # self.engine.setProperty('voice', voices[0].id)

        print("timer time", self.timer_time)

        # return_value = True
        # a running function cannot be stopped functionality for crons
        self.handel_calling(
            per_iteration_time, available_total_time)
        print("waiting ends")
        return 0

    #----------qq-----------
    # values=events.items()
    # #cur is iterator for keys in dictionary as per indexing
    # for cur in range(len(values)):
# obj = timed_timer()
# obj.claculate()
