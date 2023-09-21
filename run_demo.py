# from src.create_ui import create_ui
import sys
sys.path.append("/content/src")
from ui import create_ui


def main():
    demo = create_ui()
    demo.queue()
    demo.launch()


if __name__ == "__main__":
    
    main()