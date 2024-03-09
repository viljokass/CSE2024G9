Feature: Order price validation
    As a user, I want to buy stock

    Scenario: Bid is accepted
        Given current market last trade price is "100.00" as M1
        When I submit "bid" with price of M1 x "1.08" with quantity of "100"
        Then order is accepted
    
    Scenario: Offer is accepted
        Given current market last trade price is "100.00" as M1
        When I submit "offer" with price of M1 x "0.90" with quantity of "100"
        Then order is accepted

    Scenario: Bid is rejected
        Given current market last trade price is "100.00" as M1
        When I submit "bid" with price of M1 x "1.11" with quantity of "100"
        Then order is rejected

    Scenario: Offer is rejected
        Given current market last trade price is "100.00" as M1
        When I submit "offer" with price of M1 x "-1.01" with quantity of "100"
        Then order is rejected