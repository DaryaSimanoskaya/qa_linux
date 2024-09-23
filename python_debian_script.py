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
        total_processes += 1

        if user in user_process_count:
            user_process_count[user] += 1
        else:
            user_process_count[user] = 1

        total_mem += mem
        total_cpu += cpu

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


def generate_report(report):
    report_str = f"Отчет о состоянии системы\n"
    report_str += f"Пользователи системы: {', '.join(report['users'])}\n"
    report_str += f"Процессов запущено: {report['total_processes']}\n\n"
    report_str += f"Пользовательских процессов:\n"
    for user, count in report["user_process_count"].items():
        report_str += f"{user}: {count}\n"
    report_str += f"\nВсего памяти используется: {report['total_mem']:.1f}%\n"
    report_str += f"Всего CPU используется: {report['total_cpu']:.1f}%\n"
    report_str += f"Больше всего памяти использует: {report['max_mem_process'][0]} {report['max_mem_process'][1]:.1f}%\n"
    report_str += f"Больше всего CPU использует: {report['max_cpu_process'][0]} {report['max_cpu_process'][1]:.1f}%\n"

    return report_str


def save_report(report):
    now = datetime.datetime.now().strftime("%d-%m-%Y-%H:%M")
    filename = f"{now}-scan.txt"
    with open(filename, 'w') as f:
        f.write(generate_report(report))
    print(f"Отчёт сохранён в файл {filename}")


if __name__ == "__main__":
    report = process_info()
    report_str = generate_report(report)
    print(report_str)
    save_report(report)
