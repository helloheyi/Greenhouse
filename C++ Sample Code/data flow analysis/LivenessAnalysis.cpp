

#include "AnalysisStrategy.h"
#include "llvm/IR/Instructions.h"   // Include for StoreInst, AllocaInst, etc.
#include "llvm/Support/Casting.h"    // Include for llvm::dyn_cast and llvm::isa

namespace dataflow {
	struct LivenessAnalysis : public AnalysisStrategy{
		public:
			static char ID;
			LivenessAnalysis() : AnalysisStrategy(ID){}
			virtual ~LivenessAnalysis() {}
        /**
         * Compute the OUT set for the current instruction.
         * OUT[n] = Union of IN[n'] for each successor n'
         */
        SetVector<Value*> computeOutSet(Instruction* current) {
            SetVector<Value*> newOut;
            std::vector<Instruction*> successors = getSuccessors(current);

            for (Instruction* succ : successors) {
                SetVector<Value*>* succInSet = inMap[succ];
                // Filter out constants and non-variable instructions
                for (Value* V : *succInSet) {
                    if (isa<Instruction>(V) || isa<Argument>(V)) {
                        newOut.insert(V);
                    }
                }
            }

            return newOut;
        }


        
        /**
         * Compute the IN set for the current instruction.
         * IN[n] = use[n] ∪ (OUT[n] - def[n])
         */
        SetVector<Value*> computeInSet(Instruction* current, SetVector<Value*>& outSet) {
            SetVector<Value*> newIn;

            // Compute USE and DEF sets
            SetVector<Value*> useSet;
            SetVector<Value*> defSet;
            computeUseAndDef(current, useSet, defSet);

            // IN[n] = USE[n] ∪ (OUT[n] - DEF[n])
            newIn = outSet;
            newIn.set_subtract(defSet);
            newIn.insert(useSet.begin(), useSet.end());

            return newIn;
        }


        
        /**
         * Compute the use[n] and def[n] sets for the current instruction.
         */
        
        void computeUseAndDef(Instruction* inst, SetVector<Value*>& useSet, SetVector<Value*>& defSet) {
            // Define the value produced by this instruction
            if (!inst->getType()->isVoidTy()) {
                defSet.insert(inst);
            }

            //  Binary Operations
            if (auto* binOp = dyn_cast<BinaryOperator>(inst)) {
                for (auto* operand : inst->operands()) {
                    if (!isa<Constant>(operand)) {
                        useSet.insert(operand);
                    }
                }
                defSet.insert(inst);

            //  ICmp instructions
            } else if (auto* icmpInst = dyn_cast<ICmpInst>(inst)) {
                for (auto* operand : inst->operands()) {
                    if (!isa<Constant>(operand)) {
                        useSet.insert(operand);
                    }
                }
                defSet.insert(inst);

            //  Load instructions
            } else if (auto* loadInst = dyn_cast<LoadInst>(inst)) {
                Value* ptrOperand = loadInst->getPointerOperand();
                if (!isa<Constant>(ptrOperand)) {
                    useSet.insert(ptrOperand);
                }

            //  Store instructions
            } else if (auto* storeInst = dyn_cast<StoreInst>(inst)) {
                Value* valueOperand = storeInst->getValueOperand();
                Value* ptrOperand = storeInst->getPointerOperand();
                if (!isa<Constant>(valueOperand)) {
                    useSet.insert(valueOperand);
                }
                if (!isa<Constant>(ptrOperand)) {
                    useSet.insert(ptrOperand);
                }

            //  PHI nodes
            } else if (auto* phiInst = dyn_cast<PHINode>(inst)) {
                for (unsigned i = 0; i < phiInst->getNumIncomingValues(); ++i) {
                    Value* incomingValue = phiInst->getIncomingValue(i);
                    if (!isa<Constant>(incomingValue)) {
                        useSet.insert(incomingValue);
                    }
                }
                defSet.insert(inst);

            //  GEP (GetElementPtr)  (pointer and indices)
            } else if (auto* gepInst = dyn_cast<GetElementPtrInst>(inst)) {
                for (auto* operand : gepInst->operands()) {
                    if (!isa<Constant>(operand)) {
                        useSet.insert(operand);
                    }
                }
                defSet.insert(inst);

            //  Branch instructions
            } else if (auto* brInst = dyn_cast<BranchInst>(inst)) {
                if (brInst->isConditional()) {
                    Value* cond = brInst->getCondition();
                    if (!isa<Constant>(cond)) {
                        useSet.insert(cond);
                    }
                }

            // Generic case for other instructions
            } else {
                for (auto* operand : inst->operands()) {
                    if (!isa<Constant>(operand)) {
                        useSet.insert(operand);
                    }
                }
            }
        }


        bool updateSet(SetVector<Value*>* oldSet, SetVector<Value*>& newSet) {
            if (*oldSet != newSet) {
                *oldSet = newSet;
                return true;
            }
            return false;
        }
        
        // Evaluate function for dataflow analysis
        virtual EvalutionResult evaluate(Instruction* current) override {
            // 1: the new OUT set
            SetVector<Value*> newOutSet = computeOutSet(current);

            // 2: the new IN set based on the OUT set
            SetVector<Value*> newInSet = computeInSet(current, newOutSet);

            // 3: update the IN and OUT maps if they have changed
            bool inChanged = updateSet(inMap[current], newInSet);
            bool outChanged = updateSet(outMap[current], newOutSet);
            
            // 4: return if either IN or OUT sets changed
            if (inChanged || outChanged) {
                return EvalutionResult::Modified;
            } else {
                return EvalutionResult::Unmodified;
            }
            
            
            
        }
        
        
	
		protected:
			virtual std::string getAnalysisName() override{
				return "Liveness";
			}
	};

	char LivenessAnalysis::ID = 1;
	static RegisterPass<LivenessAnalysis> X("Liveness", "Liveness Analysis Strategy",
											false /* Only looks at CFG */,
											false /* Analysis Pass */);
}
