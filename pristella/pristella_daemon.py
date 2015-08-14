import daemon
from lockfile.pidlockfile import PIDLockFile
import os
import sys
import time
from datetime import datetime, timedelta
from .config_loader import ConfigLoader
from .app import App


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def print_log(str):
    print(time.strftime("%Y-%m-%d(%a) %H:%M:%S ") + str)


def daemon_process():
    print_log("[system] pristella begin")

    config_path = os.path.normpath(
        os.path.join(BASE_DIR, "../config/settings.json"))
    config = ConfigLoader(config_path)
    config.load()

    module = __import__(
        config.data["module"], fromlist=[config.data["app_class"]])
    app_class = getattr(module, config.data["app_class"])
    if not issubclass(app_class, App):
        print_log("[error] app_class must be subclass of App.")
        sys.exit(1)
    app = app_class(config)

    time_beg = datetime.now()
    try:
        cycle_mins = int(config.data["routine_cycle"])
        if cycle_mins < 1:
            cycle_mins = 15
    except ValueError:
        cycle_mins = 15

    cycle = timedelta(minutes=cycle_mins)
    rest_sec = 60  # 60sec. = 1min.

    # first run
    def run():
        ret = app.do()
        if ret is False:
            print_log("[error] post failed.")
        else:
            print_log("[app] post success.")

    run()

    while True:
        time_end = datetime.now()
        time_diff = time_end - time_beg

        if time_diff >= cycle:
            time_beg = time_end

            run()

            time.sleep(rest_sec)


def main():
    working_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), ".."))

    if not os.path.exists("/tmp/pristella"):
        os.makedirs("/tmp/pristella")

    context = daemon.DaemonContext(
        working_directory=working_dir,
        pidfile=PIDLockFile("/tmp/pristella/daemon.pid"),
        stdout=open(os.path.join(working_dir, "log/log.txt"), "a+"),
        stderr=open(os.path.join(working_dir, "log/error.txt"), "a+"))

    with context:
        daemon_process()


if __name__ == "__main__":
    main()
