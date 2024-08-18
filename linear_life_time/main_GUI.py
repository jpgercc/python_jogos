import datetime
import tkinter as tk
from tkinter import messagebox


def calculate_age(birth_date):
    today = datetime.datetime.now()
    age_delta = today - birth_date

    years = age_delta.days // 365
    months = (age_delta.days // 30) % 12
    days = age_delta.days % 30

    return years, months, days


def estimate_life_expectancy(age, health_factors):
    base_life_expectancy = 85

    if health_factors["smoking"]:
        base_life_expectancy -= 10
    if health_factors["obesity"]:
        base_life_expectancy -= 5
    if health_factors["healthy_diet"]:
        base_life_expectancy += 3
    if health_factors["regular_exercise"]:
        base_life_expectancy += 5

    remaining_life = max(0, base_life_expectancy - age)  # Ensure non-negative value

    return remaining_life


def calculate():
    try:
        year_birth = int(year_entry.get())
        month_birth = int(month_entry.get())
        day_birth = int(day_entry.get())
        hour_birth = int(hour_entry.get())

        birth_date = datetime.datetime(year_birth, month_birth, day_birth, hour_birth)

        years, months, days = calculate_age(birth_date)

        smoking = smoking_var.get() == 1
        obesity = obesity_var.get() == 1
        healthy_diet = healthy_diet_var.get() == 1
        regular_exercise = regular_exercise_var.get() == 1

        health_factors = {
            "smoking": smoking,
            "obesity": obesity,
            "healthy_diet": healthy_diet,
            "regular_exercise": regular_exercise
        }

        estimated_years_left = estimate_life_expectancy(years, health_factors)

        result_message = (f"You have lived {years} years, {months} months, and {days} days.\n"
                          f"Based on your current age and the information provided, you might have approximately {estimated_years_left} years left.\n"
                          )

        messagebox.showinfo("Result", result_message)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values for date and time.")


root = tk.Tk()
root.title("Life Expectancy Calculator")

tk.Label(root, text="Year of Birth:").grid(row=0, column=0)
year_entry = tk.Entry(root)
year_entry.grid(row=0, column=1)

tk.Label(root, text="Month of Birth:").grid(row=1, column=0)
month_entry = tk.Entry(root)
month_entry.grid(row=1, column=1)

tk.Label(root, text="Day of Birth:").grid(row=2, column=0)
day_entry = tk.Entry(root)
day_entry.grid(row=2, column=1)

tk.Label(root, text="Hour of Birth (24h):").grid(row=3, column=0)
hour_entry = tk.Entry(root)
hour_entry.grid(row=3, column=1)

smoking_var = tk.IntVar()
tk.Checkbutton(root, text="Smoking", variable=smoking_var).grid(row=4, column=0, sticky=tk.W)

obesity_var = tk.IntVar()
tk.Checkbutton(root, text="Obesity", variable=obesity_var).grid(row=5, column=0, sticky=tk.W)

healthy_diet_var = tk.IntVar()
tk.Checkbutton(root, text="Healthy Diet", variable=healthy_diet_var).grid(row=6, column=0, sticky=tk.W)

regular_exercise_var = tk.IntVar()
tk.Checkbutton(root, text="Regular Exercise", variable=regular_exercise_var).grid(row=7, column=0, sticky=tk.W)

calculate_button = tk.Button(root, text="Calculate", command=calculate)
calculate_button.grid(row=8, column=0, columnspan=2)

root.mainloop()