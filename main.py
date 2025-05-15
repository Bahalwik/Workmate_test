import argparse

def read_employees_from_csv(csv_files):
    employees = []
    header = dict()
    for file in csv_files:
        with open(file, mode='r') as csv_file:
            for i_line in csv_file:
                i_line = i_line.strip().split(',')
                if header:
                    employ = dict(zip(header, i_line))
                    employ.pop('email'), employ.pop('id')
                    employees.append(employ)
                else:
                    header = i_line
                    for i_category in range(len(i_line)):
                        if i_line[i_category] == 'salary' or i_line[i_category] == 'hourly_rate':
                            i_line.remove(header[i_category])
                            i_line.insert(i_category, 'rate')
                            break
            header = dict()
    return employees


csv_employees = read_employees_from_csv(['data1.csv', 'data2.csv', 'data3.csv'])


def calculate_payout(employees):
    department_payouts = dict()

    for employee in employees:
        department = employee['department']
        hours_worked = int(employee['hours_worked'])
        hourly_rate = int(employee['rate'])
        payout = hours_worked * hourly_rate

        if department not in department_payouts:
            department_payouts[department] = {'hours': hours_worked, 'payout': payout}
        else:
            department_payouts[department]['hours'] += hours_worked
            department_payouts[department]['payout'] += payout

    return department_payouts

def generate_payout_report(departments_payouts, employees):
    """Генерирует текстовый отчёт по зарплатам."""

    rows = []
    for emp in employees:
        hours = int(emp['hours_worked'])
        rate = int(emp['rate'])
        rows.append([
            emp['department'],
            emp['name'],
            f"{hours}",
            f"{rate}",
            f"{hours * rate}"
        ])

    rows.sort()
    headers = ["Department", "Name", "Hours", "Rate", "Payout"]

    col_widths = [
        max(len(headers[0]), max(len(row[0]) for row in rows)),
        max(len(headers[1]), max(len(row[1]) for row in rows)),
        max(len(headers[2]), max(len(row[2]) for row in rows)),
        max(len(headers[3]), max(len(row[3]) for row in rows)),
        max(len(headers[4]), max(len(row[4]) for row in rows))
    ]

    separator = "-" * (col_widths[0] + 3)
    empty_line = " " * (sum(col_widths) + 3 * len(col_widths) - 1)
    header = " | ".join(
        f" {h:^{w}} " for h, w in zip(headers, col_widths)
    )

    new_data = []
    departs_info = sorted(departments_payouts)
    count = 0
    check_departs = None

    for row in rows:
        if len(departs_info) != count and departs_info[count] == row[0]:
            if check_departs and check_departs != row[0]:
                formatted_row = [
                    'Total',
                    ' ' * (col_widths[1] + 3),
                    f" {departments_payouts[check_departs]['hours']:^{col_widths[2] + 20}} ",
                    f" ${departments_payouts[check_departs]['payout']:^{col_widths[4] }} "
                ]
                new_data.append(" ".join(formatted_row))
                new_data.append(empty_line)

            check_departs = departs_info[count]
            depart_string = f"{row[0]:<{col_widths[0]}}  "
            new_data.append(depart_string)
            count += 1

        elif check_departs == row[0]:
            pass

        else:
            formatted_row = [
                ' ' * col_widths[0],
                ' ' * (col_widths[1] + 3),
                f" {departs_info[count - 1]:^{col_widths[2] + 2}} ",

                ]
            new_data.append(" ".join(formatted_row))

        formatted_row = [
            separator,
            f" {row[1]:<{col_widths[1] + 2}} ",
            f" {row[2]:^{col_widths[2] + 2}} ",
            f" {row[3]:^{col_widths[3] + 2}} ",
            f" ${row[4]:<{col_widths[4] + 2}} "
        ]
        new_data.append(" ".join(formatted_row))

    formatted_row = [
        'Total',
        ' ' * (col_widths[1] + 3),
        f" {departments_payouts[check_departs]['hours']:^{col_widths[2] + 20}} ",
        f" ${departments_payouts[check_departs]['payout']:^{col_widths[4]}} "
    ]
    new_data.append(" ".join(formatted_row))
    return "\n".join([header, ("-" * (sum(col_widths) + 3 * len(col_widths) + 6))] + new_data)


REPORT_GENERATORS = {
    'payout': {
        'description': 'Total payout by department',
        'function': lambda employees: generate_payout_report(calculate_payout(employees), employees),
    # Здесь можно добавить другие отчёты
    },
}


def main():
    parser = argparse.ArgumentParser(description='Generate employee reports.')
    parser.add_argument('files', type=str, nargs='+')
    parser.add_argument('--report', type=str, required=True,
                        choices=REPORT_GENERATORS.keys(),)

    args = parser.parse_args()

    employees = read_employees_from_csv(args.files)
    if not employees:
        print("Error: No valid employee data found in the provided files.")
        return

    report_generator = REPORT_GENERATORS[args.report]['function']
    report = report_generator(employees)

    print(report)


if __name__ == '__main__':
    main()
