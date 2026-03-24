import sys
from pathlib import Path 
# Add project root to python path so 'src' module can bi imported 
project_root = Path(__file__).parent.parent 
sys.path.insert(0,str(project_root))
