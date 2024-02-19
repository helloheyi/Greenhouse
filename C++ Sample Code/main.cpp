//
//  main.cpp
//  Pricing_v2
//
//  Created by Yi He on 2024-02-19.
//

#include <iostream>
#include <vector>
#include <cmath>
#include <string>


class MarketQuote {
public:
    int days; // Days to maturity
    double rate; // Annualized SOFR rate

    MarketQuote(int d, double r) : days(d), rate(r) {}
};

class YieldCurveBuilder {
    //constructor
public:
    YieldCurveBuilder(const std::vector<MarketQuote>& inputQuotes) : quotes(inputQuotes) {
        // You can call bootstrapDiscountFactors() here if you want to automatically calculate
        // the discount factors as soon as the YieldCurveBuilder is instantiated
    }
    
private:
    std::vector<MarketQuote> quotes; // Renamed for clarity
    std::vector<double> discountFactors; // Stores discount factors for each maturity
    std::vector<double> forwardRates; // Stores forward rates between intervals
    
public:
    // Utility function for linear interpolation
    double linearInterpolate(int day) {
        if (quotes.empty()) return 1.0;
        for (size_t i = 0; i < quotes.size() - 1; ++i) {
            
            if (day >= quotes[i].days && day <= quotes[i + 1].days){
                double x0 = quotes[i].days;
                double y0 = discountFactors[i];
                double x1 = quotes[i + 1].days;
                double y1 = discountFactors[i + 1];
                return y0 + (day - x0) * (y1 - y0) / (x1 - x0);
            }
        }
        
        
        return 1.0 ;
    }
    
    // Calculate discount factor for a specific day
    void bootstrapDiscountFactors() {
        // Initialize discount factors vector with the same size
        discountFactors.resize(quotes.size(), 0.0);
        
        // Calculate the first discount factor directly from the first quote
        int firstDay = quotes[0].days;
        double firstRate = quotes[0].rate;
        discountFactors[0] = 1.0 / (1.0 + firstRate * firstDay / 360.0);
        
        // Bootstrapping subsequent discount factors
        for (size_t ii = 1; ii < quotes.size(); ++ii) {
            int currentDay = quotes[ii].days;
            double currentRate = quotes[ii].rate;
            
            // Calculate the time from the last known discount factor
            int lastDay = quotes[ii - 1].days;
            int dayDelta = currentDay - lastDay;
            
            // Calculate the current discount factor
            discountFactors[ii] = discountFactors[ii - 1] / (1.0 + currentRate * dayDelta / 360.0);
        }
    }
    
    const std::vector<double>& getDiscountFactors() const {
        return discountFactors;
    }
    
    void calculateForwardRates() {
        
        // One less forward rate than discount factors
        forwardRates.resize(quotes.size() -1 , 0.0);
        // use discount factors to get forward rates
        for (size_t ii = 0; ii < quotes.size() - 1; ++ii) {
            double D1 = discountFactors[ii];
            double D2 = discountFactors[ii+1];
            int T1 = quotes[ii].days;
            int T2 = quotes[ii + 1].days;
            forwardRates[ii] = ((1 / D2) - (1 / D1)) / (D1 * (T2 - T1)) * 360;
            
        }
        
    }
    
    const std::vector<double>& getForwardRates() const {
        return forwardRates;
    }
};
    


class SwapValuator {
    // attribute
private:
    // indicates that we are passing a reference to an instance of YieldCurveBuilder rather than making a copy of it.
    // Efficiency especially if the object is large or contains a significant amount of data
    YieldCurveBuilder& ycb;
    // swap information
    double notional;
    double fixedRate;
    int paymentFrequency;
    int maturityDays;
    std::string leg1;
    
public:
    // constructor
    SwapValuator(YieldCurveBuilder& ycBuilder, double notional, double fixedRate, int frequency, int maturity,  const std::string& leg1Status)
        : ycb(ycBuilder), notional(notional), fixedRate(fixedRate), paymentFrequency(frequency), maturityDays(maturity), leg1(leg1Status)  {}
        
    // value fix leg
    double valueFixedLeg(){
        double pv = 0.0;
        int paymentInterval =360 / paymentFrequency;
        for (int day = paymentInterval; day <= maturityDays; day += paymentInterval){
            // payment
            double payment = notional * (fixedRate / paymentFrequency);
            double df = ycb.linearInterpolate(day);
            pv += df*payment;
        }
        return pv;
    }
    
    // value float leg
    double valueFloatingLeg(){
        double pv = 0.0;
        int paymentInterval =360 / paymentFrequency;
        // Corrected to bind to a const reference: get the forward rates
        const std::vector<double>&forwardRates = ycb.getForwardRates(); // Get the forward rates

        
        for (int day = paymentInterval, ii = 0; day <= maturityDays && ii<forwardRates.size(); day += paymentInterval, ++ii){
            double forwardRate = forwardRates[ii];
            // payment
            double payment = notional * (forwardRate/ paymentFrequency);
            double df = ycb.linearInterpolate(day);
            pv += df*payment;
        }
        return pv;
    }
    
    double netSwapValue() {
        
        // Convert leg1 to lowercase for case-insensitive comparison
        std::string leg1Lower = leg1; 
        // Make a copy to transform as all low char
        std::transform(leg1Lower.begin(), leg1Lower.end(), leg1Lower.begin(),[](unsigned char c){ return std::tolower(c); });

        if (leg1Lower == "long") {
            return valueFixedLeg() - valueFloatingLeg();
        } else {
            return valueFloatingLeg() - valueFixedLeg();
        }
    }

};




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


