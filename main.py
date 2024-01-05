import argparse
from smi_to_ass.smi_to_ass import smi_to_ass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--smi_dir", type=str, default="smi")
    parser.add_argument("--save_dir", type=str, default="ass")
    parser.add_argument("--styles", type=str, default="", nargs="+")

    args = parser.parse_args()

    smi_dir = args.smi_dir
    save_dir = args.save_dir
    styles = args.styles

    smi_to_ass(
        smi_dir=smi_dir,
        save_dir=save_dir,
        styles=styles,
    )