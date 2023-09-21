from src.create_ui import create_ui

def main():
    demo = create_ui()
    demo.queue()
    demo.launch(share = True)


if __name__ == "__main__":
    
    main()
