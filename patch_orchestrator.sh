#!/bin/bash
set -e
set -x

ORCH_SCRIPT="unified_orchestrator.py"

echo "INFO: Applying patch to unified_orchestrator.py to include axis3_kb_path..."

sed -i "/axis2_kb_path=Path('data/knowledge_base/axis2_likelihoods.csv')/a             axis3_kb_path=Path('data/knowledge_base/axis3_likelihoods.csv')" "$ORCH_SCRIPT"

echo "SUCCESS: unified_orchestrator.py has been patched. The engine will now receive all three knowledge bases."