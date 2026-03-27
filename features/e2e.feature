Feature: End to end purchase flow

  @smoke
  Scenario: Full purchase journey with add remove and checkout
    Given I am on the login page
    When I login with username "standard_user" and password "secret_sauce"
    Then I should be on the inventory page

    When I add "Sauce Labs Bike Light" to the cart
    And I remove "Sauce Labs Bike Light" from the cart

    And I add "Sauce Labs Backpack" to the cart
    And I go to the cart page
    Then the cart should contain "Sauce Labs Backpack"

    When I click checkout
    And I fill details with firstname "Rashmi" lastname "S" postal "NN1"
    And I continue to checkout step two
    And I finish the order
    Then the URL should contain "checkout-complete"
    And I should see "Thank you for your order"

    When I go back to home
    Then the URL should contain "inventory"
