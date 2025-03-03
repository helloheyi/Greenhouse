
#pragma once
#include "llvm/Pass.h"
#include "llvm/IR/Function.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/IR/CFG.h"
#include "llvm/IR/ValueMap.h"
#include "llvm/ADT/SetVector.h"
#include <string>
#include "llvm/IR/InstIterator.h"

using namespace llvm;

namespace dataflow{
	/**
	 * Get the predecessors of a given instruction in the control-flow graph.
	 */
	inline std::vector<Instruction*> getPredecessors(Instruction* I){
		std::vector<Instruction*> ret;
		BasicBlock* BB = I->getParent();
		for(BasicBlock::reverse_iterator i = BB->rbegin(), e = BB->rend(); i != e; ++i){
			if (&(*i) == I){
				++i;
				if(i == e){
					for(pred_iterator pre = pred_begin(BB), BE = pred_end(BB); pre != BE;  ++pre)
						ret.push_back(&(*((*pre)->rbegin())));
				}
				else{
					ret.push_back(&(*i));
				}
				break;
			}
		}
		return ret;
	}

	/**
	 * Get the successors of a given instruction in the control-flow graph.
	 */
	inline std::vector<Instruction*> getSuccessors(Instruction* I){
		std::vector<Instruction*> ret;
		BasicBlock* BB = I->getParent();
		for(BasicBlock::iterator i = BB->begin(), e = BB->end(); i != e; ++i){
			if (&(*i) == I){
				++i;
				if(i == e){
					for(succ_iterator succ = succ_begin(BB), BS = succ_end(BB); succ != BS;  ++succ)
						ret.push_back(&(*((*succ)->begin())));
				}
				else{
					ret.push_back(&(*i));
				}
				break;
			}
		}
		return ret;
	}

	/**
	 * Check whether a given instruction defines a local variable. Note since
	 * LLVM's IR is in SSA, local variables are directly represented by the
	 * instructions defining them.
	 */
	inline bool isDef(Instruction* I){
		return !(I->getType()->isVoidTy());
	}
}
