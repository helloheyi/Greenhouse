//
//  Created by Yi He on 2024-02-19.
//
// MarketQuote.hpp
#ifndef MARKETQUOTE_HPP
#define MARKETQUOTE_HPP

#include <iostream>
class MarketQuote {
public:
    int days; // Days to maturity
    double rate; // Annualized market quote rate
    MarketQuote(int d, double r) : days(d), rate(r) {} // Constructor
    virtual~MarketQuote() {} // Destructor
};

#endif /* MARKETQUOTE_HPP */

