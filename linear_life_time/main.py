import datetime


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


def main():
    year_birth = int(input("What year you were born: "))
    month_birth = int(input("What month you were born: "))
    day_birth = int(input("What day you were born: "))
    hour_birth = int(input("Type the your hour you were born (in 24 hours format): "))

    birth_date = datetime.datetime(year_birth, month_birth, day_birth, hour_birth)

    years, months, days = calculate_age(birth_date)

    print(f"You have lived {years} years, {months} months and {days} days.")

    health_factors = {
        "smoking": input("Do you smoke? (yes/no): ").lower() == "yes",
        "obesity": input("Do you consider yourself obese? (yes/no): ").lower() == "yes",
        "healthy_diet": input("Do you generally maintain a healthy diet? (yes/no): ").lower() == "yes",
        "regular_exercise": input("Do you engage in regular exercise? (yes/no): ").lower() == "yes"
    }

    estimated_years_left = estimate_life_expectancy(years, health_factors)

    print(
        f"Based on your current age and the information provided, you might have approximately {estimated_years_left} years left.")

    print(
        "Remember, this is just an estimate. A healthy lifestyle can significantly improve your life expectancy. Consult a healthcare professional for a more accurate assessment.")


if __name__ == "__main__":
    main()