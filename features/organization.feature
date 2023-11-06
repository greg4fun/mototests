Feature: Organization management
  Scenario: Create a new organization
    Given I have the organization feature set to "ALL"
    When I request to create a new organization
    Then I should receive a confirmation of the organization creation
