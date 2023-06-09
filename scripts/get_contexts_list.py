import argparse
import json
import os

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        type=str,
        default="contexts/contexts.json",
        help="""
        The json file generated by `generate_contexts.py`.
        """,
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="contexts",
        help="The path where the unique contexts list and utterance ids will write to.",
    )
    return parser.parse_args()


def main():
    args = get_args()

    assert os.path.exists(
        args.manifest
    ), f"Recognition results : {args.manifest} does not exist."

    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)

    with open(args.manifest, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    contexts = set()
    utt_ids = []
    for k, v in manifest.items():
        contexts.update(v["contexts"])
        utt_ids.append(k)

    with open(f"{args.output_dir}/contexts.txt", "w", encoding="utf-8") as f:
        for c in contexts:
            f.write(c + "\n")
        f.flush()
    with open(f"{args.output_dir}/utt_id", "w", encoding="utf-8") as f:
        for utt in utt_ids:
            f.write(utt + "\n")
        f.flush()

if __name__ == "__main__":
    main()
