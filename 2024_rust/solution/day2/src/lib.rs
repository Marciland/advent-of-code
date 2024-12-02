extern crate helpers;

use helpers::input_to_string_vector;

fn gather_reports(input: &[String]) -> Vec<Vec<i8>> {
    let mut reports = Vec::with_capacity(input.len());

    for line in input {
        let report: Vec<i8> = line
            .split(' ')
            .map(|char| char.parse::<i8>().expect("Not a number"))
            .collect();

        reports.push(report);
    }

    reports
}

fn is_safe(report: &[i8]) -> bool {
    let mut increasing: u8 = 0;
    let mut decreasing: u8 = 0;

    // looking at couples wouldve been better
    for (index, level) in report.iter().enumerate() {
        if index == 0 || index == report.len() - 1 {
            continue;
        }

        let previous = report[index - 1];
        let next = report[index + 1];

        if level - previous == 0
            || level.abs_diff(previous) > 3
            || level - next == 0
            || level.abs_diff(next) > 3
        {
            return false;
        }

        if level > &previous {
            increasing += 1;
        } else {
            decreasing += 1;
        }

        if level > &next {
            decreasing += 1;
        } else {
            increasing += 1;
        }

        if increasing != 0 && decreasing != 0 {
            return false;
        }
    }

    true
}

fn bruteforce_report(report: &[i8]) -> bool {
    // lazy as this should still be very fast
    let mut result: Vec<bool> = Vec::with_capacity(report.len());

    for i in 0..report.len() {
        let mut modified_report = Vec::from(report);
        modified_report.remove(i);
        result.push(is_safe(&modified_report));
    }

    if result.contains(&true) {
        return true;
    }

    false
}

pub fn star1() {
    /*
       Reports are safe if:
           levels all increase or decrease
           differ by at least 1 at most 3

       collect amount of safe reports
    */
    let input: Vec<String> = input_to_string_vector(2);
    let reports = gather_reports(&input);

    let mut safe_reports = 0;
    for report in reports {
        if is_safe(&report) {
            safe_reports += 1;
        }
    }

    println!("{safe_reports}");
}

pub fn star2() {
    /*
       Same rules, but one level can be removed
    */
    let input: Vec<String> = input_to_string_vector(2);
    let reports = gather_reports(&input);

    let mut safe_reports = 0;
    for report in reports {
        if bruteforce_report(&report) {
            safe_reports += 1;
        }
    }

    println!("{safe_reports}");
}
