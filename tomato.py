#!/usr/bin/env python3

import sys
import time
import subprocess

BREAK_MINUTES, PLAN_MINUTES = 5, 5
WORK_MINUTES = 25


def main():
    try:
        if len(sys.argv) <= 1 or sys.argv[1] in ["-h", "--help"]:
            help()
        
        elif sys.argv[1] in ["-p", "--pymo"]:
            minutes = int(sys.argv[2]) if len(sys.argv) > 2 else WORK_MINUTES
            print(f'🍅 tomato {minutes} minutes. Ctrl+C to exit')
            tomato(minutes, 'It is time to take a break')

        elif sys.argv[1] in ["-p", "--pause"]:
            minutes = int(sys.argv[2]) if len(sys.argv) > 2 else BREAK_MINUTES
            print(f'🛀 break {minutes} minutes. Ctrl+C to exit')
            tomato(minutes, 'It is time to work')

    except KeyboardInterrupt:
        pass
    except Exception as ex:
        print(ex)
        exit(1)


def tomato(minutes, notify_msg):
    start_time = time.perf_counter()
    while True:
        diff_seconds = int(round(time.perf_counter() - start_time))
        left_seconds = minutes * 60 - diff_seconds
        if left_seconds <= 0:
            print('')
            break

        countdown = '{}:{} ⏰'.format(
            int(left_seconds / 60), int(left_seconds % 60))
        duration = min(minutes, 25)
        progressbar(diff_seconds, minutes * 60, duration, countdown)
        time.sleep(1)

    notify_me(notify_msg)


def progressbar(curr, total, duration=10, extra=''):
    frac = curr / total
    filled = round(frac * duration)
    print('\r', '🍅' * filled + '--' * (duration - filled)
         , '[{:.0%}]'.format(frac), extra, end='')


def notify_me(msg):
    '''
    # macos desktop notification
    terminal-notifier -> https://github.com/julienXX/terminal-notifier#download
    terminal-notifier -message <msg>

    # ubuntu desktop notification
    notify-send

    # voice notification
    say -v <lang> <msg>
    lang options:
    - Daniel:       British English
    - Ting-Ting:    Mandarin
    - Sin-ji:       Cantonese
    '''

    print(msg)
    try:
        if sys.platform == 'darwin':
            # macos desktop notification
            subprocess.run(
                ['terminal-notifier', '-title', '🍅', '-message', msg])
            subprocess.run(['say', '-v', 'Daniel', msg])
        elif sys.platform.startswith('linux'):
            # ubuntu desktop notification
            subprocess.Popen(["notify-send", '🍅', msg])
        else:
            # windows?
            # TODO: windows notification
            pass

    except:
        # skip the notification error
        pass


def help():
    appname = sys.argv[0]
    appname = appname if appname.endswith(
        '.py') else 'tomato'  # tomato is pypi package

    print('Use: pymo [OPTION]... [ARG]... [FLAG] [ARG]...')
    print('Pymo3 - forked Pomodoro technique 🍅')
    print(f'Starts pymodoro. Default time-blocks combo: {PLAN_MINUTES}m (next-TODOs) \
planning+ {WORK_MINUTES}m work + {BREAK_MINUTES}m break')

    print(f'\n')
    print(f'Options')

    print(f'\n')
    print(f'#          [N] can be any custom positive integer, if.')

    print(f'\n')
    print(
        f'-p,--pymo     [N] Starts N or {WORK_MINUTES}m work time-block (default)')
    print(f'-b,--break    [N] Starts N or  {BREAK_MINUTES}m break (default)')

    print(f'\n')
    print(f'-P,--planning [N] Starts N or  {PLAN_MINUTES}m next-TODOs planning time-\
block (default)')
    print(f'                  After, the script will display a dialog box where \
user can enter those to append it to the list file')

    print(f'\n')
    print(f'Flags (Optional, their arguments are mandatory both to --long options and -short options too)')

    print(f'\n')
    print(f'-r,--reminder          N Plays every N minutes a notification sound.')
    print(f'   --reminder-register N Displays every N minutes the list file of')
    print(f'                         next-TODOs, where user can \
select or cancel to enter the next todo to working on')


if __name__ == "__main__":
    main()
