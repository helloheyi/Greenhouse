
#ifndef VanillaOpt_hpp
#define VanillaOpt_hpp
#include <string>

#include <stdio.h>
class VanillaOpt
{
    // inside Class only
    private:
    // option parameters
        double S;
        double K;
        double r_d;
        double r_f;
        double sigma;
        double T;
        std::string Option_Type;
        // untility functions: const reduce accidental modifications.
        double norm_cdf(double x) const;
        double forward() const;
        double d1(double f) const;
        double d2(double f) const;
    
    public:
    // can be access outside class for valuation
    //constructor
    VanillaOpt(double S, double K, double r_d,double r_f, double sigma, double T, std::string Option_Type);
    // deconstructor to cleanup resources if required
    // ~VanillaOpt();
    double option_val();


    
};

#endif /* VanillaOpt_hpp */
