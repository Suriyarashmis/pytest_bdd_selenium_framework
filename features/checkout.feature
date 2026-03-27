Feature: Checkout functionality

  Background:
    Given I am logged in as "standard_user" with password "secret_sauce"
    And I add "Sauce Labs Onesie" to the cart
    And I navigate to the cart
    And I click checkout

  Scenario: Missing first name shows error
    When I fill details with firstname "EMPTY" lastname "Ashok" postal "EC1A"
    And I click continue expecting error
    Then I should see checkout error "First Name is required"

  Scenario: Missing last name shows error
    When I fill details with firstname "Ron" lastname "EMPTY" postal "EC1A"
    And I click continue expecting error
    Then I should see checkout error "Last Name is required"

  Scenario: Missing postal code shows error
    When I fill details with firstname "Ron" lastname "Ashok" postal "EMPTY"
    And I click continue expecting error
    Then I should see checkout error "Postal Code is required"

  Scenario: Cancel on step one returns to cart
    When I fill details with firstname "Ron" lastname "Ashok" postal "N7H"
    And I cancel from checkout step one
    Then the URL should contain "cart"

  Scenario: Overview page totals are correct
    When I fill details with firstname "Ron" lastname "Ashok" postal "N7H"
    And I continue to checkout step two
    Then the total should equal item price plus tax

  Scenario: Cancel on overview returns to inventory
    When I fill details with firstname "Ron" lastname "Ashok" postal "N7H"
    And I continue to checkout step two
    And I cancel from checkout step two
    Then the URL should contain "inventory"

  @smoke
  Scenario: Successful order completion
    When I fill details with firstname "Ron" lastname "Ashok" postal "N7H"
    And I continue to checkout step two
    And I finish the order
    Then I should see "Thank you for your order"
