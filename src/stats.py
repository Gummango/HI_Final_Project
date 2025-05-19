import csv
from collections import defaultdict
import matplotlib.pyplot as plt
from datetime import datetime


def plot_visit_trends(file_path, save_path="visit_trend.png"):

    visit_counts = defaultdict(int)
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                date = row['Visit_time']
                visit_counts[date] += 1

        dates = sorted(visit_counts)
        counts = [visit_counts[d] for d in dates]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, counts, marker='o')
        plt.title("Total Visits Per Day")
        plt.xlabel("Date")
        plt.ylabel("Number of Visits")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
    except Exception as e:
        print(f"Error generating visit trend plot: {e}")


def plot_insurance_distribution(file_path, save_path="insurance_distribution.png"):

    insurance_counts = defaultdict(int)
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                insurance = row["Insurance"]
                insurance_counts[insurance] += 1

        labels = list(insurance_counts.keys())
        sizes = list(insurance_counts.values())

        plt.figure(figsize=(7, 7))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.title("Patient Insurance Distribution")
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
    except Exception as e:
        print(f"Error generating insurance pie chart: {e}")


def plot_demographics_by_age(file_path, save_path="age_distribution.png"):

    ages = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    age = int(row["Age"])
                    ages.append(age)
                except ValueError:
                    continue

        plt.figure(figsize=(8, 5))
        plt.hist(ages, bins=10, edgecolor='black')
        plt.title("Age Distribution of Patients")
        plt.xlabel("Age")
        plt.ylabel("Number of Patients")
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
    except Exception as e:
        print(f"Error generating age histogram: {e}")