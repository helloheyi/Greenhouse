
#include "AnalysisStrategy.h"

namespace dataflow {
	struct ReachDefAnalysis : public AnalysisStrategy{
		public:
			static char ID;
			ReachDefAnalysis() : AnalysisStrategy(ID){}
			virtual ~ReachDefAnalysis(){};

            /**
             * Compute the IN set for the current instruction.
             * IN[n] = Union of OUT[n'] for each predecessor n'
             */
            SetVector<Value*> computeInSet(Instruction* current) {
                SetVector<Value*> newIn;
                std::vector<Instruction*> predecessors = getPredecessors(current);
                for (Instruction* pred : predecessors) {
                    SetVector<Value*>* predOut = outMap[pred];
                    // union all out
                    newIn.set_union(*predOut);
                }

                return newIn;
            }
            
            /**
             * Compute the OUT set for the current instruction.
             * OUT[n] = IN[n] ∪ GEN[n]
             */
            SetVector<Value*> computeOutSet(Instruction* current, SetVector<Value*>& newIn) {
                SetVector<Value*> newOut = newIn;

                if (isDef(current)) {
                    newOut.insert(current);
                }

                return newOut;
            }
        
            bool isDef(Instruction* inst) {
                return !(inst->getType()->isVoidTy());
            }
        
            bool updateSet(SetVector<Value*>* oldSet, SetVector<Value*>& newSet) {
                if (*oldSet != newSet) {
                    *oldSet = newSet;
                    return true;
                }
                return false;
            }
        
			virtual EvalutionResult evaluate(Instruction* current) override {
               
                //  1:  the new IN set
                SetVector<Value*> newIn = computeInSet(current);

                // 2:  the new OUT set
                SetVector<Value*> newOut = computeOutSet(current, newIn);

                //  3: update the IN and OUT maps if they have changed
                bool inChanged = updateSet(inMap[current], newIn);
                bool outChanged = updateSet(outMap[current], newOut);

                // 4: return if either IN or OUT sets changed
                if (inChanged || outChanged) {
                    return EvalutionResult::Modified;
                } else {
                    return EvalutionResult::Unmodified;
                }
                
			}

		protected:
			virtual std::string getAnalysisName() override{
				return "ReachDef";
			}
	};

	char ReachDefAnalysis::ID = 0;
	static RegisterPass<ReachDefAnalysis> X("ReachDef", "Reach Definition Analysis Strategy",
											false /* Only looks at CFG */,
											false /* Analysis Pass */);
}
