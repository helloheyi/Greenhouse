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
public:
    YieldCurveBuilder(const std::vector<MarketQuote> & inputQuotes);
    //deconstructor
    virtual ~YieldCurveBuilder(){};
    
    double linearInterpolate(int day);
    void bootstrapDiscountFactors();
    const std::vector<double>& getDiscountFactors() const;
    void calculateForwardRates();
    const std::vector<double>& getForwardRates() const;

    
private:
    std::vector<MarketQuote> quotes; 
    std::vector<double> discountFactors; 
    std::vector<double> forwardRates;
    
};

#endif 
