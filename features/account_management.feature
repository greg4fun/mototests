Feature: Account management in organization

  Scenario: Create a new account in the organization
    Given I have organization details
    When I create a new account with email "test@example.com" and account name "Test Account"
    Then the account should be successfully created

  Scenario: Invite an account to the organization
    Given I have an existing account with email "test@example.com"
    When I invite the account with email "test@example.com" to the organization
    Then the invitation should be successfully sent

  Scenario: Close an account in the organization
    Given I have an existing account with id "test-account-id"
    When I close the account with id "test-account-id"
    Then the account should be successfully closed

  Scenario: List accounts in the organization
    When I request to list accounts in the organization
    Then I should receive a list of accounts
