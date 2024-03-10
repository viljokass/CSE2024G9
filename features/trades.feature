Feature: Validate trades happen according to given logic
    As a user, I want to trade stock

    Scenario: Bid is accepted
        Given current market last trade price is "100.00" as M1
        When I submit "bid" with price of M1 x "1.00" with quantity of "100"
        And I submit "offer" with price of M1 x "0.80" with quantity of "200"
        And I submit "bid" with price of M1 x "1.01" with quantity of "200"
        And I submit "bid" with price of M1 x "0.95" with quantity of "50"
        And I submit "bid" with price of M1 x "1.00" with quantity of "30"
        And I submit "offer" with price of M1 x "1.00" with quantity of "250"
        Then there exists trades
            | time      | price             | quantity  |
            | T1        | 101.00            |  200      |
            | T1        | 100.00            |  50       |