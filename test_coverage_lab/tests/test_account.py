"""
Test Cases for Account Model
"""
import json
from random import randrange
import pytest
from models import db
from models.account import Account, DataValidationError

ACCOUNT_DATA = {}

@pytest.fixture(scope="module", autouse=True)
def load_account_data():
    """ Load data needed by tests """
    global ACCOUNT_DATA
    with open('tests/fixtures/account_data.json') as json_data:
        ACCOUNT_DATA = json.load(json_data)

    # Set up the database tables
    db.create_all()
    yield
    db.session.close()

@pytest.fixture
def setup_account():
    """Fixture to create a test account"""
    account = Account(name="John businge", email="john.businge@example.com")
    db.session.add(account)
    db.session.commit()
    return account

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    """ Truncate the tables and set up for each test """
    db.session.query(Account).delete()
    db.session.commit()
    yield
    db.session.remove()

######################################################################
#  E X A M P L E   T E S T   C A S E
######################################################################

# ===========================
# Test Group: Role Management
# ===========================

# ===========================
# Test: Account Role Assignment
# Author: John Businge
# Date: 2025-01-30
# Description: Ensure roles can be assigned and checked.
# ===========================

def test_account_role_assignment():
    """Test assigning roles to an account"""
    account = Account(name="John Doe", email="johndoe@example.com", role="user")

    # Assign initial role
    assert account.role == "user"

    # Change role and verify
    account.change_role("admin")
    assert account.role == "admin"

# ===========================
# Test: Invalid Role Assignment
# Author: John Businge
# Date: 2025-01-30
# Description: Ensure invalid roles raise a DataValidationError.
# ===========================

def test_invalid_role_assignment():
    """Test assigning an invalid role"""
    account = Account(role="user")

    # Attempt to assign an invalid role
    with pytest.raises(DataValidationError):
        account.change_role("moderator")  # Invalid role should raise an error


######################################################################
#  T O D O   T E S T S  (To Be Completed by Students)
######################################################################

"""
Each student in the team should implement **one test case** from the list below.
The team should coordinate to **avoid duplicate work**.

Each test should include:
- A descriptive **docstring** explaining what is being tested.
- **Assertions** to verify expected behavior.
- A meaningful **commit message** when submitting their PR.
"""

# TODO 1: Test Default Values
# - Ensure that new accounts have the correct default values (e.g., `disabled=False`).
# - Check if an account has no assigned role, it defaults to "user".

# TODO 2: Test Updating Account Email
# - Ensure an account’s email can be successfully updated.
# - Verify that the updated email is stored in the database.

# TODO 3: Test Finding an Account by ID
# - Create an account and retrieve it using its ID.
# - Ensure the retrieved account matches the created one.

# ===========================
# Test: Invalid Email Input
# Author: Angel V
# Date: 2026-02-03
# Description: Ensure invalid email formats are rejected.
# ===========================
# TODO 4: Test Invalid Email Handling
# - Check that invalid emails (e.g., "not-an-email") raise a validation error.
# - Ensure accounts without an email cannot be created.
def test_invalid_email_input():
    invalid_emails = [
        'plainaddress',
        'missingatsign.com',
        'missingdomain@',
        '@missingusername.com',
        'user@domain'
    ]

    for email in invalid_emails:
        account = Account(name='Test User', email=email, role='user')
        with pytest.raises(DataValidationError):
            account.validate_email()
            
# TODO Test deleting an account
# ===========================
# Test: Delete Account
# Author: Angel V
# Date: 2026-02-08
# Description: Ensure an account can be deleted from the database.
# ===========================

def test_delete_account(setup_account):
    account = setup_account
    account_id = account.id

    account.delete()                        # deleting the account
    deleted_account = Account.query.get(account_id)
    assert deleted_account is None

# TODO 5: Test Password Hashing
# ======================================
# Test: Password Hashing
# Author: Zachary Sin
# Date: 2026-02-13
# Description: Ensure that passwords are stored as **hashed values**.
#              Verify that plaintext passwords are never stored in the database.
# ======================================
def test_password_hashing(setup_account):

    # set password with set_password()
    test_password = "testpassword123!"
    setup_account.set_password(test_password)

    # check the stored password is not plaintext
    assert setup_account.password_hash != test_password

    # check the password exists and is a string
    assert setup_account.password_hash is not None
    assert isinstance(setup_account.password_hash, str)

    # check the password was stored correctly by set_password()
    assert setup_account.check_password(test_password) == True

    # check the password is not returning true for any random string
    wrong_test_password = "wrongtestpassword123!"
    assert setup_account.check_password(wrong_test_password) == False

# TODO 6: Test valid withdrawal
# - Verify that withdrawing a valid amount correctly decreases the balance.
# ===========================
# Test: Valid Withdrawal
# Author: Connor Palmira
# Date: 2026-02-10
# Description: Ensure that withdrawals of positive values reduce the balance amount correctly
# ===========================
def test_valid_withdrawal(setup_account):
    """Test successful withdrawal of positive values from account is correct"""

    account = setup_account

    with pytest.raises(DataValidationError):
        account.withdraw(0)
    with pytest.raises(DataValidationError):
        account.withdraw(-50)

    account.deposit(100)
    db.session.commit()

    balance = account.balance
    withdraw_amount = 65

    assert withdraw_amount > 0

    account.withdraw(withdraw_amount)
    db.session.commit()

    expected_amount = balance - withdraw_amount
    assert account.balance == expected_amount

# TODO 7: Test Withdrawal with Insufficient Funds
# ===========================
# Test: Withdrawal with Insufficient Funds
# Author: Thomas Feng
# Date: 2026-02-15
# Description: Ensure that withdrawing more than the available balance is not allowed.
# ===========================
def test_withdrawal_insufficient_funds():
    """Test withdrawing with insufficient funds"""
    account = Account(balance=0.0)  # Set initial balance

    # Attempt to withdraw more than the balance
    with pytest.raises(DataValidationError):
        account.withdraw(100.0)  # insufficient funds should raise an error

# TODO 8: Test Bulk Insertion
# - Create and insert multiple accounts at once.
# - Verify that all accounts are successfully stored in the database.

# TODO 9: Test Account Deactivation/Reactivate
# - Ensure accounts can be deactivated.
# - Verify that deactivated accounts cannot perform certain actions.
# - Ensure reactivation correctly restores the account.

# TODO 10: Test Email Uniqueness Enforcement
# - Ensure that duplicate emails are not allowed.
# - Verify that accounts must have a unique email in the database.

# TODO 11: Test Role-Based Access
# - Ensure users with different roles ('admin', 'user', 'guest') have appropriate permissions.
# - Verify that role changes are correctly reflected in the database.
