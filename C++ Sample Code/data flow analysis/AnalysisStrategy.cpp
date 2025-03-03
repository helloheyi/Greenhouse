
#include "AnalysisStrategy.h"
#include "IChaoticIterationAlgorithm.h"
#include "ChaoticIterationAlgorithm.cpp"

using namespace llvm;

namespace dataflow {
	bool AnalysisStrategy::runOnFunction(Function &F){
		errs() << "Running " << getAnalysisName() << " on " << F.getName() << "\n";

		ValueMap<Instruction*,SetVector<Value*>*> gradedInMap;
		ValueMap<Instruction*,SetVector<Value*>*> gradedOutMap;

		for (inst_iterator I = inst_begin(F), E= inst_end(F); I != E; ++I){
			gradedInMap[&(*I)] = new SetVector<Value*>;
			gradedOutMap[&(*I)] = new SetVector<Value*>;

			inMap[&(*I)] = gradedInMap[&(*I)];
			outMap[&(*I)] = gradedOutMap[&(*I)];
		}

		IChaoticIterationAlgorithm* chaoticIterationAlgorithm = new ChaoticIterationAlgorithm();
		chaoticIterationAlgorithm->Run(this, F);
		
		for (inst_iterator I = inst_begin(F), E= inst_end(F); I != E; ++I){
			errs() << "Instruction: " << *I << "\n";
			errs() << "In set: \n";
			SetVector<Value*>* inSet = gradedInMap[&(*I)];
			errs() << "[";
			for(SetVector<Value*>::iterator V = inSet->begin(), VE = inSet->end(); V != VE; ++V){
				errs() << **V << "; ";
			}
			errs() << "]\n";
			errs() << "Out set: \n";
			SetVector<Value*>* outSet = gradedOutMap[&(*I)];
			errs() << "[";
			for(SetVector<Value*>::iterator V = outSet->begin(), VE = outSet->end(); V != VE; ++V){
				errs() << **V << "; ";
			}
			errs() << "]\n";
			errs() << "\n";
		}
		
		for (inst_iterator I = inst_begin(F), E= inst_end(F); I != E; ++I){
			delete gradedInMap[&(*I)];
			delete gradedOutMap[&(*I)];
		}
		return false;
	}
}
