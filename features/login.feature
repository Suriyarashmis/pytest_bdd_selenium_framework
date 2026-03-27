Feature: Login functionality

  Scenario: Username only shows password required error
    Given I am on the login page
    When I enter username "random_user" and click login
    Then I should see error "Password is required"

  Scenario: Password only shows username required error
    Given I am on the login page
    When I enter password "random_sauce" and click login
    Then I should see error "Username is required"

  Scenario: Invalid credentials shows mismatch error
    Given I am on the login page
    When I login with username "random_user" and password "random_sauce"
    Then I should see error "Username and password do not match"

  Scenario: Locked out user sees locked out error
    Given I am on the login page
    When I login with username "locked_out_user" and password "secret_sauce"
    Then I should see error "locked out"

  @smoke
  Scenario: Valid credentials navigates to inventory
    Given I am on the login page
    When I login with username "standard_user" and password "secret_sauce"
    Then I should be on the inventory page
