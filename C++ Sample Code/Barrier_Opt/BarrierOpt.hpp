
#ifndef BarrierOpt_hpp
#define BarrierOpt_hpp

#include <string>
#include <stdio.h>
class BarrierOpt{
    // inside Class only
    private:
    // option parameters
        double S;
        double K;
        double r_d;
        double r_f;
        double sigma;
        double T;
        // set as default value as 0.0001
        double eps;
        double B;
        std::string Option_Type;
        std::string Knock_Type;
        double Barrier_call() const;
        double Barrier_put() const;
        int knockTypeAsInt() const;
            
    public:
    // can be access outside class for valuation
    //constructor
    BarrierOpt(double S, double K, double r_d, double r_f, double sigma, double T, double eps,double B,std::string Option_Type,std::string Knock_Type);
    // deconstructor to cleanup resources if required
    // ~VanillaOpt();
    double Barrier_val();
    
};

#endif /* BarrierOpt_hpp */
