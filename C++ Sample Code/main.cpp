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
    int days; 
    double rate; 

    MarketQuote(int d, double r) : days(d), rate(r) {}
};

class YieldCurveBuilder {
public:
    YieldCurveBuilder(const std::vector<MarketQuote>& inputQuotes) : quotes(inputQuotes) {
    }
    
private:
    std::vector<MarketQuote> quotes; 
    std::vector<double> discountFactors; 
    std::vector<double> forwardRates; 
public:
    // utility function for linear interpolation
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
    
    void bootstrapDiscountFactors() {
        // initialize discount factors vector with the same size
        discountFactors.resize(quotes.size(), 0.0);
        
        // calculate the first discount factor directly from the first quote
        int firstDay = quotes[0].days;
        double firstRate = quotes[0].rate;
        discountFactors[0] = 1.0 / (1.0 + firstRate * firstDay / 360.0);
        
        // bootstrapping subsequent discount factors
        for (size_t ii = 1; ii < quotes.size(); ++ii) {
            int currentDay = quotes[ii].days;
            double currentRate = quotes[ii].rate;
            
            // calculate the time from the last known discount factor
            int lastDay = quotes[ii - 1].days;
            int dayDelta = currentDay - lastDay;
            
            // calculate the current discount factor
            discountFactors[ii] = discountFactors[ii - 1] / (1.0 + currentRate * dayDelta / 360.0);
        }
    }
    
    const std::vector<double>& getDiscountFactors() const {
        return discountFactors;
    }
    
    void calculateForwardRates() {
        forwardRates.resize(quotes.size() -1 , 0.0);
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
        
        std::string leg1Lower = leg1; 
        std::transform(leg1Lower.begin(), leg1Lower.end(), leg1Lower.begin(),[](unsigned char c){ return std::tolower(c); });
        if (leg1Lower == "long") {
            return valueFixedLeg() - valueFloatingLeg();
        } else {
            return valueFloatingLeg() - valueFixedLeg();
        }
    }

};




    int main() {
        // step 1: Initialize Market Quotes
        std::vector<MarketQuote> quotes = {
            {30, 0.0005},  
            {90, 0.0015}, 
            {180, 0.002},  
            {360, 0.003}  
        };
        // step 2: initialize YieldCurveBuilder with the quotes
        YieldCurveBuilder ycb(quotes);
        // Step 3: calculate Discount Factors
        ycb.bootstrapDiscountFactors();
        // step 4: Calculate Forward Rates
        ycb.calculateForwardRates();
        // step 5: Print Discount Factors
        std::cout << "Discount Factors:\n";
           for (size_t i = 0; i < quotes.size(); ++i) {
               std::cout << "Days: " << quotes[i].days << ", DF: " << ycb.getDiscountFactors()[i] << "\n";
           }
           // step 6: Print Forward Rates
           std::cout << "\nForward Rates:\n";
           for (size_t i = 0; i < quotes.size() - 1; ++i) { 
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
        std::cout << "Net Swap Value: " << sv.netSwapValue() << std::endl;
};


