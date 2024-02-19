//
//  YieldCurveBuilder.hpp
//  YieldCurve_Swap
//
//  Created by Yi He on 2024-02-19.
//

#ifndef YieldCurveBuilder_hpp
#define YieldCurveBuilder_hpp
#include "MarketQuote.hpp"
#include <iostream>
#include <vector>
#include <cmath>
#include <string>

class YieldCurveBuilder {
    //constructor
public:
    YieldCurveBuilder(const std::vector<MarketQuote> & inputQuotes);
        // You can call bootstrapDiscountFactors() here if you want to automatically calculate
        // the discount factors as soon as the YieldCurveBuilder is instantiated
    
    //deconstructor
    virtual ~YieldCurveBuilder(){};
    
    double linearInterpolate(int day);
    void bootstrapDiscountFactors();
    const std::vector<double>& getDiscountFactors() const;
    void calculateForwardRates();
    const std::vector<double>& getForwardRates() const;

    
private:
    std::vector<MarketQuote> quotes; // Renamed for clarity
    std::vector<double> discountFactors; // Stores discount factors for each maturity
    std::vector<double> forwardRates; // Stores forward rates between intervals
    
};

#endif /* YieldCurveBuilder_hpp */
