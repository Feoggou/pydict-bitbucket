from gi.repository import Notify
from threading import Timer
from time import sleep

count_times = 0

Notify.init("Hello world")


def show_notification(message: str):
    notif_obj = Notify.Notification.new("Hello world", message, "dialog-information")
    notif_obj.show()


def timer_callback(count):
    show_notification("Moowahahahahaha!")

    count += 1
    if count < 3:
        timer = Timer(5, timer_callback, [count])
        timer.start()


timer = Timer(2, timer_callback, [count_times])
timer.start()