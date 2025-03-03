//
//  Option.hpp
//  UpdateBarrier_Opt
//
//  Created by Yi He on 2025-03-02.
//

#ifndef Option_hpp
#define Option_hpp
#include <stdio.h>

enum class OptionType { Call, Put };
///  base class for all option types.
class Option
{
protected:
    double S;
    double K;
    double r_d;
    double r_f;
    double sigma;
    double T;
    OptionType type;

public:
    Option(double S_, double K_, double rd_, double rf_, double sigma_, double T_, OptionType type_)
    : S(S_), K(K_), r_d(rd_), r_f(rf_), sigma(sigma_), T(T_), type(type_) {}

    // virtual destructor so derived classes clean up correctly
    virtual ~Option() {}

    // pure virtual method for pricing
    virtual double Price() const = 0;

    OptionType GetType() const { return type; }
};


#endif /* Option_hpp */
