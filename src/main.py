import pandas as pd
import matplotlib.pyplot as plt


def load_data():
    return pd.read_csv("data/raw_data.csv")


def clean_data(df):
    original_rows = len(df)
    missing_age = df["Age"].isnull().sum()
    missing_email = df["Email"].isnull().sum()
    missing_salary = df["Salary"].isnull().sum()
    duplicates_removed = df.duplicated().sum()

    df = df.drop_duplicates().reset_index(drop=True)
    cleaned_rows = len(df)

    df["Age"] = df["Age"].fillna(df["Age"].mean())
    df["Email"] = df["Email"].fillna("unknown@example.com")
    df["Salary"] = df["Salary"].fillna(df["Salary"].mean())
    df["Department"] = df["Department"].str.upper()

    return (
        df,
        original_rows,
        cleaned_rows,
        duplicates_removed,
        missing_age,
        missing_email,
        missing_salary
    )


def validate_data(df):
    invalid_age = (df["Age"] < 0).sum()
    invalid_salary = (df["Salary"] < 0).sum()

    return invalid_age, invalid_salary


def generate_department_report(df):
    department_summary = df.groupby("Department").agg(
        Employee_Count=("Name", "count"),
        Average_Salary=("Salary", "mean")
    )

    print("\nDepartment Summary:")
    print(department_summary)

    department_summary.to_csv("reports/department_summary.csv")

    return department_summary


def create_visualization(department_summary):
    department_summary["Average_Salary"].plot(kind="bar")

    plt.title("Average Salary by Department")
    plt.xlabel("Department")
    plt.ylabel("Average Salary")
    plt.tight_layout()

    plt.savefig("reports/average_salary_by_department.png")
    plt.close()


def generate_report(
    original_rows,
    cleaned_rows,
    duplicates_removed,
    missing_age,
    missing_email,
    missing_salary,
    invalid_age,
    invalid_salary
):
    report = f"""
DATA CLEANING REPORT
--------------------
Original rows: {original_rows}
Cleaned rows: {cleaned_rows}
Duplicates removed: {duplicates_removed}

MISSING VALUES
--------------
Missing Age values: {missing_age}
Missing Email values: {missing_email}
Missing Salary values: {missing_salary}

DATA VALIDATION
---------------
Invalid Age values: {invalid_age}
Invalid Salary values: {invalid_salary}
"""

    with open("reports/cleaning_report.txt", "w") as file:
        file.write(report)


def main():
    # Load data
    df = load_data()

    # Clean data
    (
        df,
        original_rows,
        cleaned_rows,
        duplicates_removed,
        missing_age,
        missing_email,
        missing_salary
    ) = clean_data(df)

    # Generate department report
    department_summary = generate_department_report(df)

    # Create visualization
    create_visualization(department_summary)

    # Validate data
    invalid_age, invalid_salary = validate_data(df)

    print("\nData Validation:")
    print("Invalid Age values:", invalid_age)
    print("Invalid Salary values:", invalid_salary)

    # Display cleaned data
    print("\nCleaned data:")
    print(df)

    df.to_csv("output/cleaned_data.csv", index=False)

    # Display final data quality
    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    # Display cleaning report summary
    print("\nDATA CLEANING REPORT")
    print("--------------------")
    print("Original rows:", original_rows)
    print("Cleaned rows:", cleaned_rows)
    print("Duplicates removed:", duplicates_removed)
    print("Missing Age values:", missing_age)
    print("Missing Email values:", missing_email)
    print("Missing Salary values:", missing_salary)

    # Generate report file
    generate_report(
        original_rows,
        cleaned_rows,
        duplicates_removed,
        missing_age,
        missing_email,
        missing_salary,
        invalid_age,
        invalid_salary
    )


if __name__ == "__main__":
    main()