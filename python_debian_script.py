import subprocess
import datetime


def parse_ps_aux():
    result = subprocess.run(['ps', 'aux'], stdout=subprocess.PIPE)
    ps_output = result.stdout.decode('utf-8').splitlines()
    return ps_output[1:]

def process_info():
    ps_output = parse_ps_aux()
    users = set()
    total_processes = 0
    user_process_count = {}
    total_mem = 0.0
    total_cpu = 0.0
    max_mem_process = ("", 0.0)
    max_cpu_process = ("", 0.0)

    for line in ps_output:
        columns = line.split(None, 10)
        user = columns[0]
        cpu = float(columns[2])
        mem = float(columns[3])
        process_name = columns[10][:20]

        users.add(user)
        total_processes +=1
        
        if user in user_process_count:
            user_process_count[user] += 1 
        else:
            user_process_count[user] = 1
        total_mem+=mem
        total_cpu+=cpu

        if mem > max_mem_process[1]:
            max_mem_process = (process_name, mem)
        if cpu > max_cpu_process[1]:
            max_cpu_process = (process_name, cpu)
    return {
        "users": users,
        "total_processes": total_processes,
        "user_process_count": user_process_count,
        "total_mem": total_mem,
        "total_cpu": total_cpu,
        "max_mem_process": max_mem_process,
        "max_cpu_process": max_cpu_process
    }

def save_report(report):
    now = datetime.datetime.now().strftime("%d-%m-%Y-%H:%M")
    filename = f"{now}-scan.txt"
    with open(filename, 'w') as f:
        f.write(f"Отчет о состоянии системы\n")
        f.write(f"Пользователи системы: {', '.join(report['users'])}\n")
        f.write(f"Процессов запущено: {report['total_processes']}\n\n")
        f.write(f"Пользовательских процессов:\n")
        for user, count in report["user_process_count"].items():
            f.write(f"{user}: {count}\n")
        f.write(f"\nВсего памяти используется: {report['total_mem']:.1f}%\n")
        f.write(f"\nВсего CPU используется: {report['total_cpu']:.1f}%\n")
        f.write(f"Больше всего памяти использует: {report['max_mem_process'][0]} {report['max_mem_process'][1]:.1f}%\n")
        f.write(f"Больше всего CPU использует: {report['max_cpu_process'][0]} {report['max_cpu_process'][1]:.1f}%\n")

if __name__ == "__main__":
    report = process_info()
    print(f"Отчет о состоянии системы\n")
    print(f"Пользователи системы: {', '.join(report['users'])}\n")
    print(f"Процессов запущено: {report['total_processes']}\n\n")
    print(f"Пользовательских процессов:\n")
    for user, count in report["user_process_count"].items():
        print(f"{user}: {count}\n")
    print(f"\nВсего памяти используется: {report['total_mem']:.1f}%\n")
    print(f"\nВсего CPU используется: {report['total_cpu']:.1f}%\n")
    print(f"Больше всего памяти использует: {report['max_mem_process'][0]} {report['max_mem_process'][1]:.1f}%\n")
    print(f"Больше всего CPU использует: {report['max_cpu_process'][0]} {report['max_cpu_process'][1]:.1f}%\n")

    save_report(report)