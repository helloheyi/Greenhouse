//
//  VanillaOpt.hpp
//  UpdateBarrier_Opt
//
//  Created by Yi He on 2025-03-02.
//

#ifndef VanillaOpt_hpp
#define VanillaOpt_hpp
#include "Option.hpp"
#include <stdio.h>


#include "Option.hpp"

// A standard vanilla European option
class VanillaOption : public Option
{
public:
    // inherit the base constructor to reduce reduency
    using Option::Option;

    // valuation function
    virtual double Price() const override;

private:
    double norm_cdf(double x) const;
    double forward() const;
    double d1(double f) const;
    double d2(double f) const;
};


#endif /* VanillaOpt_hpp */
