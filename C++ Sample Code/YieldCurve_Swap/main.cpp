//
//  main.cpp
//  YieldCurve_Swap
//
//  Created by Yi He on 2024-02-19.
//
#include <iostream>
#include <vector>
#include <cmath>
#include <string>
#include "SwapValuator.hpp"


int main() {
    // step 1: initialize Market Quotes
    std::vector<MarketQuote> quotes = {
        {30, 0.0005},  
        {90, 0.0015}, 
        {180, 0.002},  
        {360, 0.003}   
    };
    
    // step 2: initialize YieldCurveBuilder with the quotes
    YieldCurveBuilder ycb(quotes);

    // step 3: calculate Discount Factors
    ycb.bootstrapDiscountFactors();
    
    // step 4: calculate Forward Rates
    ycb.calculateForwardRates();
    
    // step 5: Print Discount Factors
    std::cout << "Discount Factors:\n";
       for (size_t i = 0; i < quotes.size(); ++i) {
           std::cout << "Days: " << quotes[i].days << ", DF: " << ycb.getDiscountFactors()[i] << "\n";
       }

       // Step 6: Print Forward Rates
       std::cout << "\nForward Rates:\n";
       for (size_t i = 0; i < quotes.size() - 1; ++i) { // Forward rates are one less than discount factors
           std::cout << "From Day " << quotes[i].days << " to Day " << quotes[i + 1].days
                     << ", Forward Rate: " << ycb.getForwardRates()[i] << "\n";
       }
    // Set up a swap valuation
    double notional = 1000000; 
    double fixedRate = 0.02; 
    int paymentFrequency = 4; 
    int maturityDays = 360;
    std::string leg1 = "LONG";
    SwapValuator sv(ycb, notional, fixedRate, paymentFrequency,maturityDays,leg1);
    // calculate and output the net swap value
    std::cout << "Net Swap Value: " << sv.netSwapValue() << std::endl;
    
};


