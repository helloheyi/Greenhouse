//
//  Digital_Opt.hpp
//  UpdateBarrier_Opt
//
//  Created by Yi He on 2025-03-02.
//

#ifndef Digital_Opt_hpp
#define Digital_Opt_hpp
#include "Option.hpp"

#include <stdio.h>
class DigitalOption : public Option
{
private:
    // small difference for strike spread
    double eps;

public:
    DigitalOption(double S_, double K_, double rd_, double rf_,
                  double sigma_, double T_, OptionType type_,
                  double eps_)
    : Option(S_, K_, rd_, rf_, sigma_, T_, type_), eps(eps_) {}

    virtual double Price() const override;
};

#endif /* Digital_Opt_hpp */
