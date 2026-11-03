# ============================================================
# BUDGETKO: A Digital Expenses and Income Tracker
# ITE 260 - Computer Programming 1 | Period 2 Milestone
# Group 1 - BSIT, PHINMA Cagayan de Oro College - Puerto Campus
# ============================================================

# ============================================================
# STEP 1: DATA STRUCTURES
# Modules 5 & 9
# ============================================================

# Each income entry: [source, amount, schedule]
# Each expense entry: [category, amount, description]

income_records = []
expense_records = []

INCOME_SOURCES = [
    "Allowance",
    "Wages",
    "Stipend",
    "Other Support"
]

EXPENSE_CATEGORIES = [
    "Food",
    "Transportation",
    "School Supplies",
    "Personal"
]


# ============================================================
# STEP 2: INPUT VALIDATION
# Module 6
# ============================================================

def get_positive_amount(prompt):
    """
    Keeps asking until the user enters a valid
    number greater than 0.
    """
    while True:
        raw_value = input(prompt)

        try:
            amount = float(raw_value)

            if amount > 0:
                return amount
            else:
                print(
                    "[ERROR] Amount must be greater than 0. "
                    "Please try again."
                )

        except ValueError:
            print("[ERROR] Please enter a valid number.")


def get_valid_choice(prompt, options):
    """
    Displays numbered choices and returns
    the selected option.
    """
    while True:
        print(prompt)

        for index, option in enumerate(options, start=1):
            print(f"   {index}. {option}")

        raw_choice = input("Choose a number: ")

        if raw_choice.isdigit():
            choice = int(raw_choice)

            if 1 <= choice <= len(options):
                return options[choice - 1]

        print(
            "[ERROR] Invalid choice. "
            "Please select a valid number.\n"
        )


def get_whole_number(prompt):
    """
    Keeps asking until the user enters
    a whole number greater than 0.
    """
    while True:
        raw_value = input(prompt)

        if raw_value.isdigit() and int(raw_value) > 0:
            return int(raw_value)

        print(
            "[ERROR] Please enter a whole number "
            "greater than 0."
        )


def get_yes_no(prompt):
    """
    Gets a Yes or No response from the user.
    """
    while True:
        answer = input(prompt).strip().lower()

        if answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            print("[ERROR] Please enter Y or N.")


# ============================================================
# STEP 3: CALCULATION FUNCTIONS
# ============================================================

def calculate_totals(income_list, expense_list):
    """
    Returns:
    total income,
    total expenses,
    available balance.
    """

    total_income = 0.0
    total_expenses = 0.0

    # Calculate total income
    for entry in income_list:
        total_income = total_income + entry[1]

    # Calculate total expenses
    for entry in expense_list:
        total_expenses = total_expenses + entry[1]

    # Balance is income minus expenses
    balance = total_income - total_expenses

    return total_income, total_expenses, balance


# ============================================================
# STEP 4: CORE FEATURES
# Module 8
# ============================================================

# ------------------------------------------------------------
# FEATURE 1: MULTI-SOURCE INCOME LOGGING
# ------------------------------------------------------------

def add_income(income_list):
    """
    Records an income entry with source,
    amount, and schedule.
    """

    print("\n" + "=" * 50)
    print("ADD INCOME")
    print("=" * 50)

    source = get_valid_choice(
        "Select income source:",
        INCOME_SOURCES
    )

    amount = get_positive_amount(
        "Enter income amount: P"
    )

    schedule = get_valid_choice(
        "How often does this income arrive?",
        [
            "One-time / Lump-sum",
            "Weekly",
            "Monthly"
        ]
    )

    income_list.append([
        source,
        amount,
        schedule
    ])

    print(
        f"\n[SUCCESS] Logged P{amount:.2f} "
        f"from {source} ({schedule})."
    )


# ------------------------------------------------------------
# FEATURE 2: EXPENSE CATEGORIZATION
# WITH SPENDING WARNING
# ------------------------------------------------------------

def add_expense(expense_list, income_list):
    """
    Records a categorized expense.

    Before recording the expense, the system checks
    the user's current available balance.

    If the expense exceeds the balance, the system
    gives a warning but still allows the user to
    record the transaction.
    """

    print("\n" + "=" * 50)
    print("ADD EXPENSE")
    print("=" * 50)

    category = get_valid_choice(
        "Select expense category:",
        EXPENSE_CATEGORIES
    )

    amount = get_positive_amount(
        "Enter expense amount: P"
    )

    description = input(
        "Enter a short description: "
    ).strip()

    # Calculate current balance before adding expense
    total_income, total_expenses, balance = calculate_totals(
        income_list,
        expense_list
    )

    print(
        f"\nCurrent Available Balance: P{balance:.2f}"
    )

    # Check whether expense exceeds current balance
    if amount > balance:

        excess_amount = amount - balance

        print("\n" + "=" * 50)
        print("[WARNING] This expense exceeds your")
        print(f"available balance by P{excess_amount:.2f}.")
        print(
            "[ALERT] Recording this expense will "
            "make your balance negative."
        )
        print("=" * 50)

        confirm = get_yes_no(
            "\nDo you still want to record this expense? (Y/N): "
        )

        if not confirm:
            print(
                "\n[CANCELLED] Expense was not recorded."
            )
            return

    # Save expense
    expense_list.append([
        category,
        amount,
        description
    ])

    # Calculate new balance
    new_total_income, new_total_expenses, new_balance = (
        calculate_totals(
            income_list,
            expense_list
        )
    )

    print(
        f"\n[SUCCESS] Logged P{amount:.2f} "
        f"expense under {category}."
    )

    print(
        f"Remaining Balance: P{new_balance:.2f}"
    )

    # Immediate alert after recording
    if new_balance < 0:
        print(
            f"[ALERT] You are over your logged income "
            f"by P{abs(new_balance):.2f}."
        )
    elif new_balance == 0:
        print(
            "[ALERT] Your available balance is now P0.00."
        )


# ------------------------------------------------------------
# FEATURE 3: VIEW TRANSACTIONS
# ------------------------------------------------------------

def view_transactions(income_list, expense_list):
    """
    Displays all recorded income and expenses.
    """

    print("\n" + "=" * 60)
    print("INCOME RECORDS")
    print("=" * 60)

    if len(income_list) == 0:

        print("No income logged yet.")

    else:

        for i, entry in enumerate(
            income_list,
            start=1
        ):
            print(
                f"{i}. {entry[0]:<18} | "
                f"P{entry[1]:>10.2f} | "
                f"{entry[2]}"
            )

    print("\n" + "=" * 60)
    print("EXPENSE RECORDS")
    print("=" * 60)

    if len(expense_list) == 0:

        print("No expenses logged yet.")

    else:

        for i, entry in enumerate(
            expense_list,
            start=1
        ):
            print(
                f"{i}. {entry[0]:<18} | "
                f"P{entry[1]:>10.2f} | "
                f"{entry[2]}"
            )

    print("=" * 60)


# ------------------------------------------------------------
# FEATURE 4: BALANCE & SPENDING-PACE ALERT
# ------------------------------------------------------------

def check_spending_pace(income_list, expense_list):
    """
    Calculates current spending pace and determines
    whether the user may run out of money before
    the next expected income.
    """

    print("\n" + "=" * 60)
    print("BALANCE & SPENDING-PACE ALERT")
    print("=" * 60)

    total_income, total_expenses, balance = (
        calculate_totals(
            income_list,
            expense_list
        )
    )

    print(f"Total Income:       P{total_income:.2f}")
    print(f"Total Expenses:     P{total_expenses:.2f}")
    print(f"Available Balance:  P{balance:.2f}")

    # If the user already has no available funds
    if balance <= 0:

        print("\n" + "=" * 60)

        if balance < 0:
            print(
                f"[ALERT] Your expenses exceed your "
                f"logged income by P{abs(balance):.2f}."
            )
        else:
            print(
                "[ALERT] Your available balance is P0.00."
            )

        print("!" * 60)
        return

    # Ask for tracking period
    days_tracked = get_whole_number(
        "\nHow many days have you been tracking expenses? "
    )

    days_until_income = get_whole_number(
        "How many days until your next expected income? "
    )

    # Calculate average daily spending
    daily_spending_rate = (
        total_expenses / days_tracked
    )

    # Calculate how much the user may spend safely each day
    safe_daily_budget = (
        balance / days_until_income
    )

    # Project future spending
    projected_spending = (
        daily_spending_rate *
        days_until_income
    )

    print("\n" + "-" * 60)
    print("SPENDING ANALYSIS")
    print("-" * 60)

    print(
        f"Average Daily Spending:     "
        f"P{daily_spending_rate:.2f}"
    )

    print(
        f"Recommended Daily Limit:    "
        f"P{safe_daily_budget:.2f}"
    )

    print(
        f"Projected Spending:         "
        f"P{projected_spending:.2f}"
    )

    print("-" * 60)

    # Decision-making logic
    if projected_spending > balance:

        shortfall = (
            projected_spending - balance
        )

        print("[ALERT] Your current spending pace")
        print(
            "may cause you to run out of money "
            "before your next income."
        )

        print(
            f"Estimated Shortfall: "
            f"P{shortfall:.2f}"
        )

        print(
            f"Suggested Daily Limit: "
            f"P{safe_daily_budget:.2f}"
        )

    elif projected_spending == balance:

        print(
            "[NOTICE] Your current spending pace "
            "would use your balance exactly "
            "before your next income."
        )

        print(
            f"Daily Spending Limit: "
            f"P{safe_daily_budget:.2f}"
        )

    else:

        remaining_after_projection = (
            balance - projected_spending
        )

        print(
            "[OK] Your current spending pace "
            "is within your available balance."
        )

        print(
            f"Estimated Remaining Funds: "
            f"P{remaining_after_projection:.2f}"
        )

        print(
            f"Recommended Daily Limit: "
            f"P{safe_daily_budget:.2f}"
        )

    print("=" * 60)


# ------------------------------------------------------------
# FEATURE 5: STIPEND PLANNER
# ------------------------------------------------------------

def stipend_planner():
    """
    Divides a lump-sum stipend or allowance
    into a suggested budget per period.
    """

    print("\n" + "=" * 60)
    print("STIPEND PLANNER")
    print("=" * 60)

    lump_sum = get_positive_amount(
        "Enter the lump-sum amount to plan: P"
    )

    period_type = get_valid_choice(
        "Spread this across:",
        ["Weeks", "Months"]
    )

    num_periods = get_whole_number(
        f"How many {period_type.lower()} "
        "should this cover? "
    )

    amount_per_period = (
        lump_sum / num_periods
    )

    print(
        f"\n[PLAN] Suggested budget: "
        f"P{amount_per_period:.2f} per "
        f"{period_type[:-1].lower()}."
    )

    print(
        f"This plan covers {num_periods} "
        f"{period_type.lower()}."
    )

    # Suggested category breakdown
    print("\nSuggested Category Breakdown:")

    split_percentages = {
        "Food": 0.40,
        "Transportation": 0.30,
        "School Supplies": 0.10,
        "Personal": 0.10
    }

    for category, percentage in (
        split_percentages.items()
    ):

        category_amount = (
            amount_per_period *
            percentage
        )

        print(
            f"   {category:<18}: "
            f"P{category_amount:.2f} "
            f"({int(percentage * 100)}%)"
        )


# ------------------------------------------------------------
# FEATURE 6: IMPROVED REPORT
# ------------------------------------------------------------

def view_report(income_list, expense_list):
    """
    Displays:
    - total income
    - total expenses
    - available balance
    - expense total per category
    - percentage of total expenses per category
    """

    total_income, total_expenses, balance = (
        calculate_totals(
            income_list,
            expense_list
        )
    )

    print("\n" + "=" * 60)
    print("              BUDGETKO EXPENSE REPORT")
    print("=" * 60)

    # Financial summary
    print("\nFINANCIAL SUMMARY")
    print("-" * 60)

    print(
        f"Total Income:          P{total_income:.2f}"
    )

    print(
        f"Total Expenses:        P{total_expenses:.2f}"
    )

    print(
        f"Available Balance:     P{balance:.2f}"
    )

    # Expense category report
    print("\n" + "-" * 60)
    print("EXPENSES BY CATEGORY")
    print("-" * 60)

    if total_expenses == 0:

        print("No expenses have been recorded yet.")

    else:

        for category in EXPENSE_CATEGORIES:

            category_total = 0.0

            # Find total expenses for this category
            for entry in expense_list:

                if entry[0] == category:
                    category_total = (
                        category_total + entry[1]
                    )

            # Calculate percentage
            category_percentage = (
                category_total /
                total_expenses
            ) * 100

            print(f"\n{category}")
            print(
                f"   Total Spent: "
                f"P{category_total:.2f}"
            )

            print(
                f"   Percentage: "
                f"{category_percentage:.2f}%"
            )

    print("\n" + "-" * 60)
    print(
        f"TOTAL EXPENSES:     P{total_expenses:.2f}"
    )

    print(
        f"REMAINING BALANCE:  P{balance:.2f}"
    )

    # Overall balance warning
    if balance < 0:

        print("\n[ALERT]")
        print(
            f"Expenses exceed logged income by "
            f"P{abs(balance):.2f}."
        )

    elif balance == 0:

        print("\n[ALERT]")
        print(
            "Your available balance is P0.00."
        )

    else:

        print("\n[STATUS]")
        print(
            "You still have available funds "
            "based on your logged transactions."
        )

    print("=" * 60)


# ============================================================
# STEP 5: CONSOLE MENU & CONTROL LOOP
# Module 7
# ============================================================

def main():

    while True:

        print("\n" + "=" * 45)
        print("             BUDGETKO SYSTEM")
        print("=" * 45)

        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Transactions")
        print("4. View Balance & Spending Alert")
        print("5. Stipend Planner")
        print("6. View Report")
        print("7. Exit")

        choice = input(
            "\nChoose an option: "
        )

        if choice == "1":

            add_income(income_records)

        elif choice == "2":

            add_expense(
                expense_records,
                income_records
            )

        elif choice == "3":

            view_transactions(
                income_records,
                expense_records
            )

        elif choice == "4":

            check_spending_pace(
                income_records,
                expense_records
            )

        elif choice == "5":

            stipend_planner()

        elif choice == "6":

            view_report(
                income_records,
                expense_records
            )

        elif choice == "7":

            print(
                "\nThank you for using BudgetKo. "
                "Goodbye!"
            )

            break

        else:

            print(
                "[ERROR] Invalid option. "
                "Please choose 1-7."
            )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()