//
//  BarrierOpt.hpp
//  UpdateBarrier_Opt
//
//  Created by Yi He on 2025-03-02.
//

#ifndef BarrierOpt_hpp
#define BarrierOpt_hpp
#include "Option.hpp"

#include <stdio.h>
#include <string>
//  specify up-and-out, up-and-in, down-and-out, etc.
enum class BarrierType { UpOut, DownOut, UpIn, DownIn };

class BarrierOption : public Option
{
private:
    double B;
    BarrierType bType;
    double eps;
    double BarrierCall() const;
    double BarrierPut()  const;
    int knockTypeAsInt() const;

public:
    BarrierOption(double S_, double K_, double rd_, double rf_,
                  double sigma_, double T_, OptionType type_,
                  double barrier_, BarrierType bType_, double eps_ = 1.0e-4)
    : Option(S_, K_, rd_, rf_, sigma_, T_, type_),
      B(barrier_), bType(bType_), eps(eps_) {}

    virtual double Price() const override;

};

#endif /* BarrierOpt_hpp */
