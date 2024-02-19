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
    // Step 1: Initialize Market Quotes
    std::vector<MarketQuote> quotes = {
        {30, 0.0005},  // Example: 30 days, 0.05% rate
        {90, 0.0015},  // Example: 90 days, 0.15% rate
        {180, 0.002},  // Example: 180 days, 0.20% rate
        {360, 0.003}   // Example: 360 days, 0.30% rate
    };
    
    // Step 2: Initialize YieldCurveBuilder with the quotes
    YieldCurveBuilder ycb(quotes);

    // Step 3: Calculate Discount Factors
    ycb.bootstrapDiscountFactors();
    
    // Step 4: Calculate Forward Rates
    ycb.calculateForwardRates();
    
    // Step 5: Print Discount Factors
   
    
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
    double notional = 1000000; // Example notional
    double fixedRate = 0.02; // Example fixed rate
    int paymentFrequency = 4; // Quarterly payments
    int maturityDays = 360; // 1-year swap
    std::string leg1 = "LONG";
    
    SwapValuator sv(ycb, notional, fixedRate, paymentFrequency,maturityDays,leg1);
    
    // Calculate and output the net swap value
    std::cout << "Net Swap Value: " << sv.netSwapValue() << std::endl;
    
};


