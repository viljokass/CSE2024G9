Feature: Input quantity validation
  As a user, I want to trade stock

  Scenario: Order quantity is zero, order is rejected
    Given current market last trade price is "200" as M2
    When I submit "bid" with price of "200" and quantity of "0"
    Then order is rejected

  Scenario: Bid quantity is not a integer, order is rejected
    Given current market last trade price is "200" as M2
    When I submit "bid" with price of "200" and quantity of "10.1"
    Then order is rejected

  Scenario: Order quantity is negative, order is rejected
    Given current market last trade price is "200" as M2
    When I submit "offer" with price of "200" and quantity of "-100"
    Then order is rejected